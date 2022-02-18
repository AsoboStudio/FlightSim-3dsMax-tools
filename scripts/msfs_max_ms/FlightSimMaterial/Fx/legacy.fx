float4 PS_LEGACY(vOut IN) : SV_Target
{
	float2 uv = IN.UV.xy;

	float4 vColor = IN.VertexColor;
	float4 baseColor = p_baseColorTex.Sample(wrapSampler, uv);

	float detailMaskKH = 1.0;
	if (p_detailColorEnabled || p_detailNormalEnabled || p_detailOccRoughMetalEnabled)
	{
		detailMaskKH = IN.VertexColor.a * baseColor.a;
		vColor.a = 1.0;
	}

	baseColor *= p_baseColorFactor;

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
		baseColor = lerp( blendColor, baseColor, blend);
	}
	else // detail
	{		
		if (p_detailColorEnabled)
		{		
			float4 detailColor = p_detailColorTex.Sample(wrapSampler, uv * p_detailUVScale * worldMatrix[0][0] + float2(p_detailUVOffsetX, p_detailUVOffsetY));
			detailColor.xyz *= 2.0;
			detailColor.w *= detailMaskKH;
			detailColor.xyz = lerp(float3(1, 1, 1), detailColor.xyz, detailColor.w);
			baseColor.xyz = saturate(baseColor.xyz * detailColor.xyz);
			//return float4(pow(abs(p_detailColorTex.Sample(wrapSampler, uv * p_detailUVScale + float2(p_detailUVOffsetX, p_detailUVOffsetY)).x - 0.5) * 2.0, 0.2) * IN.VertexColor.x, 0, 0, 1.0);
		}
	}

	baseColor *= vColor;
	float3 emissiveColor = p_emissiveFactor.xyz * p_emissiveTex.Sample(wrapSampler, uv).xyz;

	float3 tangentNormal = 2.0 * (p_normalTex.Sample(wrapSampler, uv).xyz - 0.5);
	//blend
	if (p_blendmaskEnabled)
	{
		float3 blendTangentNormal = 0;
		if (p_detailNormalEnabled)
		{
			blendTangentNormal = 2.0 * (p_detailNormalTex.Sample(wrapSampler, uv * p_detailUVScale + float2(p_detailUVOffsetX, p_detailUVOffsetY)).xyz - 0.5);
		}
		tangentNormal = lerp(blendTangentNormal, tangentNormal, blend);
	}
	else // detail
	{
		float3 detailTangentNormal = 0;
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

	tangentNormal = normalize(tangentNormal);


	float3 worldNormal = mul(TBN, tangentNormal);


	float dotlight = saturate(dot( worldNormal.xyz, IN.LightVector));
	float ambient = (dotlight-1.f)*0.25+1.f;
	float light = saturate(dotlight)*2.f/3.f + ambient/3.f;

	float4 o;
	o.rgb = saturate(baseColor.rgb * light + emissiveColor);
	o.a = baseColor.a;

	if (p_alphaMode == 1)
	{
		if (o.a<=p_alphaCutoff)
			discard;
	}
	else if (p_alphaMode == 2 || p_alphaMode == 3) // Stochastic transparency for Nitrous
	{
		if (o.a <= gradientNoise((IN.Position2.xy/IN.Position2.w)*0.5*viewportSize))
			discard;
	}

	o.a = 1.0;
	return	o;
}