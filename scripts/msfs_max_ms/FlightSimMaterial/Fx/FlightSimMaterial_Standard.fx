#include "core.fx"
float4 PS_STANDARD(vOut IN) : SV_Target
{
	float2 uv = IN.UV.xy;
	
	float4 albedo = p_baseColorTex.Sample(wrapSampler, uv); //albedo
	float3 occ_rough_metal = p_occlusionRoughnessMetallicTex.Sample(wrapSampler, uv); //occlusion/roughness/metal
	float occlusion = occ_rough_metal.r *p_occlusionStrength;
	float roughness = occ_rough_metal.g * p_roughnessFactor;
	float metalness = occ_rough_metal.b *p_metallicFactor;	
	float4 vColor = IN.VertexColor;
	float emissiveMultiplier = p_EmissiveMultiplierFactor;
	float detailMaskKH = 1.0;
	if (p_detailColorEnabled || p_detailNormalEnabled || p_detailOccRoughMetalEnabled)
	{
		detailMaskKH = IN.VertexColor.a * albedo.a;
		vColor.a = 1.0;
	}
	albedo *= p_baseColorFactor;
	//blend part.
	float blend = 1.0;
	if (p_blendmaskEnabled)
	{
		blend = p_blendMaskTex.Sample(wrapSampler, uv).x;
		
		blend = linearstep(saturate(blend - p_blendThreshold), saturate(blend + p_blendThreshold), IN.VertexColor.a);
		float4 blendColor = p_baseColorFactor;
		if (p_detailColorEnabled)
		{
			blendColor = p_detailColorTex.Sample(wrapSampler, uv * p_detailUVScale + float2(p_detailUVOffsetX, p_detailUVOffsetY));
			//fake display gamma correct
			//blendColor.xyz = pow(blendColor.xyz, 2.2);
		} 
		albedo = lerp( blendColor, albedo, blend);
	}
	else // detail 
	{ 
		if (p_detailColorEnabled)
		{
			float4 detailColor = p_detailColorTex.Sample(wrapSampler, uv * p_detailUVScale * worldMatrix[0][0] + float2(p_detailUVOffsetX, p_detailUVOffsetY));
			detailColor.xyz *= 2.0;
			detailColor.w *= detailMaskKH;
			detailColor.xyz = lerp(float3(1, 1, 1), detailColor.xyz, detailColor.w);
			albedo.xyz = saturate(albedo.xyz * detailColor.xyz);
			//return float4(pow(abs(p_detailColorTex.Sample(wrapSampler, uv * p_detailUVScale + float2(p_detailUVOffsetX, p_detailUVOffsetY)).x - 0.5) * 2.0, 0.2) * IN.VertexColor.x, 0, 0, 1.0);
		}
	}
	albedo *= vColor;
	//albedo.rgb = lerp(occlusion, albedo, albedo.a);
	float3 emissiveColor = p_emissiveFactor.xyz * p_emissiveTex.Sample(wrapSampler, uv).xyz * emissiveMultiplier;
	float3 tangentNormal = 2.0 * (p_normalTex.Sample(wrapSampler, uv).xyz - 0.5);
	
	//blend
	if (p_blendmaskEnabled)
	{        
		float3 blendTangentNormal = float3(0,0,1);
		if (p_detailNormalEnabled)
		{            
			blendTangentNormal = 2.0 * (p_detailNormalTex.Sample(wrapSampler, uv * p_detailUVScale + float2(p_detailUVOffsetX, p_detailUVOffsetY)).xyz - 0.5) * p_detailNormalScale;
		}		
		
		tangentNormal = lerp(tangentNormal,blendTangentNormal, 1 - blend);   
	
	}

	else // detail
	{		
		float3 detailTangentNormal = float3(0,0,1);
		
		if (p_detailNormalEnabled)
		{
			float3 detailTangentNormal = 2.0 * (p_detailNormalTex.Sample(wrapSampler, uv * p_detailUVScale * worldMatrix[0][0] + float2(p_detailUVOffsetX, p_detailUVOffsetY)).xyz - 0.5) * p_detailNormalScale;
			detailTangentNormal = lerp(float3(0, 0, 1), detailTangentNormal, detailMaskKH);
			tangentNormal += detailTangentNormal;			
		}
	}
	tangentNormal.y = -tangentNormal.y;	
	tangentNormal.xy *= p_normalScale;
	tangentNormal.z = sqrt(saturate(1.f - dot(tangentNormal.xy, tangentNormal.xy)));
    float3x3 TBN = float3x3(normalize(IN.WorldTangent), normalize(IN.WorldBinormal),normalize(IN.WorldNormal)); //transforms world=>tangent space
	TBN = transpose(TBN);	
	
	float3 worldNormal = mul(TBN, normalize(tangentNormal)); //N	

	if(p_pearlescentEnabled)
	{
		float3 Lo = normalize(viewIMatrix[3].xyz - IN.wPos);
		float NdotV = 1.0f - saturate(dot(worldNormal,Lo));
		float pearlShiftRamp = pow(NdotV, p_pearlShift);
		float3 yuvCol = RGBToYUV(albedo.xyz);
		float pearlCos, pearlSin;
		sincos(-pearlShiftRamp * p_pearlRange * 6.2831853f, pearlSin, pearlCos);
		yuvCol.yz = Rotate2D(yuvCol.yz, pearlCos, pearlSin) * 3.1415926f;
		yuvCol.x = saturate(yuvCol.x + saturate(pearlShiftRamp) * p_pearlBrightness);
		albedo.xyz = lerp(albedo.xyz, saturate(YUVToRGB(yuvCol)), metalness);
	}	

	pbrLighting lighting = PBRModel(IN, worldNormal, albedo, metalness, roughness);
    
	float4 o = float4(lighting.ambientLight + lighting.directLight+ emissiveColor, albedo.a);
	o = Alpha(o,IN,p_alphaMode);
	
	return	o; 
}

////////TECHNIQUES////////
//Group: https://msdn.microsoft.com/en-us/library/windows/desktop/ff476120(v=vs.85).aspx
//Technique: https://msdn.microsoft.com/en-us/library/windows/desktop/ff476122(v=vs.85).aspx
//State Groups: https://msdn.microsoft.com/en-us/library/windows/desktop/ff476121(v=vs.85).aspx
technique11 Tech_Base
{
	pass p0
	{
        SetVertexShader(CompileShader(vs_5_0,VS_BASE()));
        SetGeometryShader( NULL );
		SetPixelShader(CompileShader(ps_5_0,PS_STANDARD()));
	}
}
technique11 Tech_TwoSide
{
	pass p0
	{
		SetRasterizerState(TwoSide);
        SetVertexShader(CompileShader(vs_5_0,VS_BASE()));
        SetGeometryShader( NULL );
		SetPixelShader(CompileShader(ps_5_0,PS_STANDARD()));
	}
}
technique11 Tech_Legacy
{
	pass p0
	{
        SetVertexShader(CompileShader(vs_5_0,VS_BASE()));
        SetGeometryShader( NULL );
		SetPixelShader(CompileShader(ps_5_0,PS_LEGACY()));
	}
}

