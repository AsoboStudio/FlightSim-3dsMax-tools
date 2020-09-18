//string ParamID = "0x0"; // default Max parser
//string ParamID = "0x003"; //scene parser
string ParamID = "0x0001"; // DXSAS parser

////////CONSTANTES////////
float4x4 worldMatrix 			: World;
float4x4 viewMatrix				: View;
float4x4 projMatrix 			: Projection;
float4x4 worldViewProjMatrix 	: WorldViewProj;
float4x4 worldIMatrix 			: WorldI;
float4x4 WorldITXf				: WorldInverseTranspose;
float4x4 viewIMatrix 			: ViewI;
float4x4 viewInverseMatrix		: ViewInverse;
//float time 						: TIME;
float2 viewportSize				: VIEWPORTPIXELSIZE;

////////APP->VERTEX////////
int texcoord0 : Texcoord
<
	int Texcoord = 0;
	int MapChannel = 1; //UV1
>;
int texcoord1 : Texcoord
<
	int Texcoord = 1;
	int MapChannel = 2; //UV2
>;
int texcoord2 : Texcoord
<
	int Texcoord = 2;
	int MapChannel = 0; //COLOR
>;
int texcoord3 : Texcoord
<
	int Texcoord = 3;
	int MapChannel = -2; //ALPHA
>;
struct a2v {
	float4 Position 	: POSITION;
	float3 Normal 		: NORMAL;
	float2 UV 			: TEXCOORD0;
	float2 UV2 			: TEXCOORD1;
	float3 VertexColor 	: TEXCOORD2;
	float VertexAlpha 	: TEXCOORD3;
	float3 Tangent		: TANGENT;
	float3 Binormal		: BINORMAL;
};

////////MATERIAL PARAMS////////
uniform float4 p_baseColorFactor<
	string UIName = "p_baseColorFactor";
	> = {1,1,1,1};
uniform float4 p_SSSColorFactor<
	string UIName = "p_SSSColorFactor";
	> = {1,1,1,1};
uniform float p_occlusionStrength<
	string UIName = "p_occlusionStrength";
	> = 1;
uniform float p_roughnessFactor<
	string UIName = "p_roughnessFactor";
	> = 1;
uniform float p_metallicFactor<
	string UIName = "p_metallicFactor";
	> = 1;
uniform float4 p_emissiveFactor<
	string UIName = "p_emissiveFactor";
	> = {0,0,0,0};
uniform float p_normalScale<
	string UIName = "p_normalScale";
	> = 1;

uniform int p_alphaMode<
	string UIName = "p_alphaMode";
	> = 0;
uniform int p_drawOrder<
	string UIName = "p_drawOrder";
	> = 0;
uniform float p_alphaCutoff<
	string UIName = "p_alphaCutoff";
	> = 0.5;
uniform float p_detailUVScale<
	string UIName = "p_detailUVScale";
	> = 2.0;
uniform float p_detailUVOffsetX<
	string UIName = "p_detailUVOffsetX";
	> = 0.0;
uniform float p_detailUVOffsetY<
	string UIName = "p_detailUVOffsetY";
	> = 0.0;
uniform float p_detailNormalScale <
	string UIName = "p_detailNormalScale";
	> = 1.0;
uniform float p_blendThreshold <
	string UIName = "p_blendThreshold";
	> = 0.1;
uniform float p_glassReflectionMaskFactor <
	string UIName = "p_glassReflectionMaskFactor";
	> = 0.0;
uniform float p_glassDeformationFactor <
	string UIName = "p_glassDeformationFactor";
	> = 0.0;
uniform float p_parallaxScale<
	string UIName = "p_parallaxScale";
	> = 0.0;
uniform float p_roomSizeXScale <
	string UIName = "p_roomSizeXScale";
	> = 0.0;
uniform float p_roomSizeYScale <
	string UIName = "p_roomSizeYScale";
	> = 0.0;
uniform float p_roomNumberXY <
	string UIName = "p_roomNumberXY";
	> = 0.0;
uniform float p_fresnelFactor <
	string UIName = "p_fresnelFactor";
	> = 0.0;
uniform float p_fresnelOpacityOffset <
	string UIName = "p_fresnelOpacityOffset";
	> = 0.0;

uniform const bool p_blendmaskEnabled <
	string UIName = "p_blendmaskEnabled";
	> = false;

uniform const bool p_detailColorEnabled <
	string UIName = "p_detailColorEnabled";
	> = false;

uniform const bool p_detailNormalEnabled <
	string UIName = "p_detailNormalEnabled";
	> = false;

uniform const bool p_detailOccRoughMetalEnabled <
	string UIName = "p_detailOccRoughMetalEnabled";
	> = false;

uniform const bool p_heightMapEnabled <
	string UIName = "p_heightMapEnabled";
	> = false;
	
////////LIGHTS////////
uniform float3 p_lightDir : DIRECTION < 
	string UIName = "p_lightDir";
	string Object = "TargetLight";
	int RefID = 0;
	>;

////////TEXTURES////////
Texture2D <float4> p_baseColorTex : DIFFUSEMAP< 
	string UIName = "p_baseColorTex";
	>;
Texture2D <float4> p_occlusionRoughnessMetallicTex< 
	string UIName = "p_occlusionRoughnessMetallicTex";
	>;
Texture2D <float4> p_normalTex< 
	string UIName = "p_normalTex";
	>;
Texture2D <float4> p_blendMaskTex< 
	string UIName = "p_blendMaskTex";
	>;
Texture2D <float4> p_wetnessAOTex< 
	string UIName = "p_wetnessAOTex";
	>;
Texture2D <float4> p_dirtTex <
	string UIName = "p_dirtTex";
	> ;
Texture2D <float4> p_heightMapTex <
	string UIName = "p_heightMapTex";
	> ;
Texture2D <float4> p_opacityTex <
	string UIName = "p_opacityTex";
	> ;
Texture2D <float4> p_emissiveTex< 
	string UIName = "p_emissiveTex";
	>;
Texture2D <float4> p_detailColorTex<
	string UIName = "p_detailColorTex";
	>;
Texture2D <float4> p_detailOcclusionRoughnessMetallicTex< 
	string UIName = "p_detailOcclusionRoughnessMetallicTex";
	>;
Texture2D <float4> p_detailNormalTex<
	string UIName = "p_detailNormalTex";
	>;


SamplerState wrapSampler
{
	FILTER = ANISOTROPIC;
	MaxAnisotropy = 8;
	AddressU = WRAP;
	AddressV = WRAP;
};
SamplerState clampSampler
{
	FILTER = ANISOTROPIC;
	MaxAnisotropy = 8;
	AddressU = CLAMP;
	AddressV = CLAMP;
};

////////VERTEX////////
struct vOut {
	float4 Position 	: SV_Position;
	float4 Position2 	: TEXCOORD0; //unjittered position
	float4 UV 			: TEXCOORD1;
	float4 VertexColor 	: TEXCOORD2;
	float3 LightVector 	: TEXCOORD3;
	float3 WorldNormal	: TEXCOORD4;
	float3 WorldTangent	: TEXCOORD5;
	float3 WorldBinormal: TEXCOORD6;
	float4 wPos			: TEXCOORD7;
};

float linearstep( float lo, float hi, float input )
{
	return saturate( (input-lo) / (hi-lo) );
}

vOut VS_BASE(a2v IN)
{
	vOut OUT;
	
	OUT.UV.xy = IN.UV;
	OUT.UV.zw = IN.UV2;
	
	//light world -> object space
	float3 lightVec = p_lightDir;
	//float3 lightVec = mul(p_lightDir, (float3x3)worldMatrix);
	lightVec = normalize(lightVec);
	
	float3 viewPos = mul(viewIMatrix[3], worldIMatrix).xyz;
	float3 viewVec = normalize(viewPos - IN.Position.xyz);
	
	OUT.Position = mul(IN.Position, worldViewProjMatrix);
	OUT.VertexColor = float4(IN.VertexColor, IN.VertexAlpha);
	OUT.LightVector = lightVec;

	OUT.WorldNormal = mul(IN.Normal, (float3x3)worldMatrix).xyz;
	OUT.WorldTangent = mul(IN.Tangent, (float3x3)worldMatrix).xyz;
	OUT.WorldBinormal = mul(IN.Binormal, (float3x3)worldMatrix).xyz;
	OUT.wPos = mul(IN.Position, worldMatrix);
	
	float4x4 projMatrix_NoJitt = projMatrix;
	projMatrix_NoJitt._m20 = projMatrix_NoJitt._m21 = 0.f;
	float4x4 worldViewProjMatrix_NoJitt = mul(mul(worldMatrix,viewMatrix),projMatrix_NoJitt);
	OUT.Position2 = mul(IN.Position, worldViewProjMatrix_NoJitt);
	
	return OUT;
}

////////PIXEL////////

float gradientNoise(float2 pixelPos)
{
	return frac( 52.9829189f * frac( dot( pixelPos, float2(0.06711056f,0.00583715f) ) ) );
}

float median(float3 v)
{
    return max(min(v.x, v.y), min(max(v.x, v.y), v.z));
}

float4 PS_BASE(vOut IN) : SV_Target
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


float RandomWindow(float2 p)
{
	p += float2(0, 12545.54);
	p = frac(p*0.3183099 + .1);
	p *= 17.0;
	return frac(p.x*p.y*(p.x + p.y));
}

float4 computeTangentialInteriorParallax(in float2 uv, in float3 eyeUV, in float cellCount, in float3 _RoomSize)
{

	float3 positionCell = frac(float3(uv, 0) / _RoomSize);
	eyeUV /= _RoomSize;

	float2 indexCell = floor(uv.xy / _RoomSize.xy);

	float randomFromCell = RandomWindow(float2(floor(indexCell.x / 1.0/*cellCount*/), indexCell.y));
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
		if (p_heightMapEnabled)
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
		if (p_heightMapEnabled)
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
		if (!p_heightMapEnabled)
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
		if (p_heightMapEnabled)
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

	float randomFromCell = RandomWindow(float2(floor(indexCell.x / cellCount), indexCell.y));
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

RasterizerState TwoSide
{
	CullMode = NONE;
};

BlendState Additif
{
	BlendEnable[0] = TRUE;
	SrcBlend[0] = ONE;
	DestBlend[0] = ONE;
	BlendOp[0] = ADD;
};

technique11 Tech_Base
{
	pass p0
	{
        SetVertexShader(CompileShader(vs_5_0,VS_BASE()));
        SetGeometryShader( NULL );
		SetPixelShader(CompileShader(ps_5_0,PS_BASE()));
	}
}

technique11 Tech_TwoSide
{
	pass p0
	{
		SetRasterizerState(TwoSide);
        SetVertexShader(CompileShader(vs_5_0,VS_BASE()));
        SetGeometryShader( NULL );
		SetPixelShader(CompileShader(ps_5_0,PS_BASE()));
	}
}

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

technique11 Tech_Additif
{
	pass p0
	{
		SetBlendState(Additif, float4(0.f,0.f,0.f,0.f), 0xFFFFFFFF);
        SetVertexShader(CompileShader(vs_5_0,VS_BASE()));
        SetGeometryShader( NULL );
		SetPixelShader(CompileShader(ps_5_0,PS_BASE()));
	}
}
