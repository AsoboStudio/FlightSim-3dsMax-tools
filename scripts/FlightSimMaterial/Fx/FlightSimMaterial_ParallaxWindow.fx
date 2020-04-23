#include "core.fx"

float4 computeTangentialInteriorParallax(in float2 uv, in float3 eyeUV, in float cellCount, in float3 _RoomSize)
{

	float3 positionCell = frac(float3(uv, 0) / _RoomSize);
	eyeUV /= _RoomSize;

	float2 indexCell = floor(uv.xy / _RoomSize.xy);

	float randomFromCell = randomValue(float2(floor(indexCell.x / 1.0/*cellCount*/), indexCell.y));
	float blindsModel = fmod(floor(randomFromCell * 37), 3.0);
	float offsetX = floor(randomFromCell * cellCount) * 1.0;
	float offsetY = floor(blindsModel) * 1.0;

	float4 uvMaxDist = float4(1.0f, 1.0f, 1.0f, 100000.0f);
	{
		// Ground
		float isGroundVisible = step(0.0f, eyeUV.y);
		float distToGround = (positionCell.y / eyeUV.y);
		float3 intersectPos = positionCell - distToGround * eyeUV;
		intersectPos.z /= _RoomSize.z;

		float groundX;
		if (p_corridorEnabled)
		{
			groundX = intersectPos.x;
		}
		else
		{
			groundX = lerp(intersectPos.x * 0.5 + 0.25, intersectPos.x, frac(intersectPos.z));
		}

		float testDistance = step(distToGround, uvMaxDist.w) * isGroundVisible;
		uvMaxDist = lerp(uvMaxDist, float4(groundX,
			-intersectPos.z * 0.25,
			0.0f,
			distToGround),
			testDistance);

		// Roof
		float isRoofVisible = 1.0f - isGroundVisible;
		float distToRoof = (-(1.0f - positionCell.y) / eyeUV.y);
		intersectPos = positionCell - distToRoof * eyeUV;
		intersectPos.z /= _RoomSize.z;
		float roofX;
		if (p_corridorEnabled)
		{
			roofX = intersectPos.x;
		}
		else
		{
			roofX = lerp(intersectPos.x * 0.5 + 0.25, intersectPos.x, frac(intersectPos.z));
		}

		testDistance = step(distToRoof, uvMaxDist.w) * isRoofVisible;
		uvMaxDist = lerp(uvMaxDist, float4(roofX,
			intersectPos.z * 0.25 + 1.0,
			0.0f,
			distToRoof),
			testDistance);

		// Left wall
		if (!p_corridorEnabled)
		{
			float isLeftVisible = step(0.0f, eyeUV.x);
			float distToLeft = ((positionCell.x) / eyeUV.x);
			intersectPos = positionCell - distToLeft * eyeUV;
			intersectPos.z /= _RoomSize.z;

			testDistance = step(distToLeft, uvMaxDist.w) * isLeftVisible;
			uvMaxDist = lerp(uvMaxDist, float4(intersectPos.z * -0.25f,
				lerp(intersectPos.y * 0.5 + 0.25, intersectPos.y, frac(intersectPos.z)),
				0.0f,
				distToLeft),
				testDistance);

			// Right wall
			float isRightVisible = 1.0f - isLeftVisible;
			float distToRight = (-(1.0f - positionCell.x) / eyeUV.x);
			intersectPos = positionCell - distToRight * eyeUV;
			intersectPos.z /= _RoomSize.z;

			testDistance = step(distToRight, uvMaxDist.w) * isRightVisible;
			uvMaxDist = lerp(uvMaxDist, float4(intersectPos.z * 0.25f + 1.0f,
				lerp(intersectPos.y * 0.5 + 0.25, intersectPos.y, frac(intersectPos.z)),
				0.0f,
				distToRight),
				testDistance);
		}

		// Back wall
		float cellDepth = _RoomSize.z;
		float distToBack = cellDepth / eyeUV.z;
		intersectPos = positionCell - distToBack * eyeUV;

		testDistance = step(distToBack, uvMaxDist.w);

		float backX;
		if (p_corridorEnabled)
		{
			backX = intersectPos.x;
		}
		else
		{
			backX = intersectPos.x*0.5 + 0.25;
		}

		uvMaxDist = lerp(uvMaxDist, float4(backX, intersectPos.y*0.5 + 0.25,
			0.0f,
			distToBack),
			testDistance);

		return float4((uvMaxDist.x + offsetX) * (1.0 / cellCount) + (1.0 / cellCount), (uvMaxDist.y + offsetY) * (1.0 / cellCount) + (1.0 / cellCount), 0, 0);
	}
}

float4 computeInteriorParallax(in float3 uv, in float3 eyeUV, in float cellCount, in float3 _RoomSize)
{

	float3 positionCell = frac(uv / _RoomSize);
	eyeUV /= _RoomSize;

	float3 indexCell = floor(uv.xyz / _RoomSize.xyz);

	float randomFromCell = randomValue(float2(floor(indexCell.x / cellCount), indexCell.y));
	float blindsModel = fmod(floor(randomFromCell * 37), min(1,cellCount));
	float offsetX = floor(randomFromCell * cellCount) * 1.0;
	float offsetY = floor(blindsModel) * 1.0;

	float4 uvMaxDist = float4(1.0f, 1.0f, 1.0f, 100000.0f);
	{
		// Ground
		float isGroundVisible = step(0.0f, eyeUV.y);
		float distToGround = (positionCell.y / eyeUV.y);
		float3 intersectPos = positionCell - distToGround * eyeUV;
		intersectPos.z /= _RoomSize.z;

		float testDistance = step(distToGround, uvMaxDist.w) * isGroundVisible;
		uvMaxDist = lerp(uvMaxDist, float4(lerp(intersectPos.x * 0.5 + 0.25, intersectPos.x, frac(intersectPos.z)),
			-intersectPos.z * 0.25,
			0.0f,
			distToGround),
			testDistance);

		// Roof
		float isRoofVisible = 1.0f - isGroundVisible;
		float distToRoof = (-(1.0f - positionCell.y) / eyeUV.y);
		intersectPos = positionCell - distToRoof * eyeUV;
		intersectPos.z /= _RoomSize.z;

		testDistance = step(distToRoof, uvMaxDist.w) * isRoofVisible;
		uvMaxDist = lerp(uvMaxDist, float4(lerp(intersectPos.x * 0.5 + 0.25, intersectPos.x, frac(intersectPos.z)),
			intersectPos.z * 0.25 + 1.0,
			0.0f,
			distToRoof),
			testDistance);

		// Left wall
		float isLeftVisible = step(0.0f, eyeUV.x);
		float distToLeft = ((positionCell.x) / eyeUV.x);
		intersectPos = positionCell - distToLeft * eyeUV;
		intersectPos.z /= _RoomSize.z;

		testDistance = step(distToLeft, uvMaxDist.w) * isLeftVisible;
		uvMaxDist = lerp(uvMaxDist, float4(intersectPos.z * -0.25f,
			lerp(intersectPos.y * 0.5 + 0.25, intersectPos.y, frac(intersectPos.z)),
			0.0f,
			distToLeft),
			testDistance);

		// Right wall
		float isRightVisible = 1.0f - isLeftVisible;
		float distToRight = (-(1.0f - positionCell.x) / eyeUV.x);
		intersectPos = positionCell - distToRight * eyeUV;
		intersectPos.z /= _RoomSize.z;

		testDistance = step(distToRight, uvMaxDist.w) * isRightVisible;
		uvMaxDist = lerp(uvMaxDist, float4(intersectPos.z * 0.25f + 1.0f,
			lerp(intersectPos.y * 0.5 + 0.25, intersectPos.y, frac(intersectPos.z)),
			0.0f,
			distToRight),
			testDistance);

		// Back wall
		float cellDepth = _RoomSize.z;
		float distToBack = cellDepth / eyeUV.z;
		intersectPos = positionCell - distToBack * eyeUV;

		testDistance = step(distToBack, uvMaxDist.w);
		uvMaxDist = lerp(uvMaxDist, float4(intersectPos.x*0.5 + 0.25, intersectPos.y*0.5 + 0.25,
			0.0f,
			distToBack),
			testDistance);

		return float4((uvMaxDist.x + offsetX) * (1.0 / cellCount) + (1.0 / cellCount), (uvMaxDist.y + offsetY) * (1.0 / cellCount) + (1.0 / cellCount), 0, 0);
	}
}


float4 PS_PARALLAX(vOut IN) : SV_Target
{
	float3x3 TBN = float3x3(normalize(IN.WorldTangent), normalize(IN.WorldBinormal),normalize(IN.WorldNormal)); //transforms world=>tangent space
	TBN = transpose(TBN);

	float2 uv = IN.UV.xy;
	float2 uv2 = IN.UV.zw;

	float parallax = p_parallaxScale;
	float3 eyevec = normalize(viewInverseMatrix[3].xyz - IN.wPos.xyz);
	float3 eyeUV = mul(eyevec, TBN); eyeUV.y *= -1;
	
	float4 tParallax = computeTangentialInteriorParallax(uv2, eyeUV, p_roomNumberXY, float3(p_roomSizeXScale, p_roomSizeYScale, p_parallaxScale));
	uv2 = tParallax.xy;

	float4 vColor = IN.VertexColor;
	float4 baseColor = p_baseColorTex.Sample(wrapSampler, uv);
	
	if (p_detailColorEnabled)
	{
		float4 blendColor = p_detailColorTex.Sample(wrapSampler, uv2);
		//fake display gamma correct
		blendColor.xyz = pow(blendColor.xyz, 2.2);
		baseColor.xyz = lerp(blendColor.xyz, baseColor.xyz, baseColor.w);
	}
		
	baseColor *= p_baseColorFactor;
	baseColor *= vColor;
	float3 emissiveColor = p_emissiveFactor.xyz * p_emissiveTex.Sample(wrapSampler, uv2).xyz;
	emissiveColor *= (1 - baseColor.w);
	emissiveColor += baseColor * (1 - baseColor.w) * 0.15;

	float3 tangentNormal = float3(0,0,1);
	//blend	
	if (p_detailNormalEnabled)
	{
		tangentNormal = 2.0 * (p_detailNormalTex.Sample(wrapSampler, uv).xyz - 0.5);
	}

	tangentNormal.y = -tangentNormal.y;
	tangentNormal.xy *= p_normalScale;
	tangentNormal.z = sqrt(saturate(1.f - dot(tangentNormal.xy, tangentNormal.xy)));

	tangentNormal = normalize(tangentNormal);
	float3 worldNormal = mul(TBN, tangentNormal);


	float dotlight = saturate(dot(worldNormal.xyz, IN.LightVector));
	float ambient = (dotlight - 1.f)*0.25 + 1.f;
	float light = saturate(dotlight)*2.f / 3.f + ambient / 3.f;

	float4 o;
	o.rgb = saturate(baseColor.rgb * light + emissiveColor);
	o.a = baseColor.a;

	if (p_alphaMode == 1)
	{
		if (o.a <= p_alphaCutoff)
			discard;
	}
	else if (p_alphaMode == 2 || p_alphaMode == 3) // Stochastic transparency for Nitrous
	{
		if (o.a <= gradientNoise((IN.Position2.xy / IN.Position2.w)*0.5*viewportSize))
			discard;
	}

	o.a = 1.0;
	return	o;
}

////////TECHNIQUES////////
//Group: https://msdn.microsoft.com/en-us/library/windows/desktop/ff476120(v=vs.85).aspx
//Technique: https://msdn.microsoft.com/en-us/library/windows/desktop/ff476122(v=vs.85).aspx
//State Groups: https://msdn.microsoft.com/en-us/library/windows/desktop/ff476121(v=vs.85).aspx

technique11 Tech_Parallax
{
	pass p0
	{
		SetVertexShader(CompileShader(vs_5_0, VS_BASE()));
		SetGeometryShader(NULL);
		SetPixelShader(CompileShader(ps_5_0, PS_PARALLAX()));
	}
}

technique11 Tech_Parallax_TwoSide
{
	pass p0
	{
		SetRasterizerState(TwoSide);
		SetVertexShader(CompileShader(vs_5_0, VS_BASE()));
		SetGeometryShader(NULL);
		SetPixelShader(CompileShader(ps_5_0, PS_PARALLAX()));
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
