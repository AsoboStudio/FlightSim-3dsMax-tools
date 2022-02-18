///////CONSTANTS///////
static const float3 Fdielectric = 0.04;
static const float Epsilon = 0.00001;

#include "utility.fx"
#include "maxdata.fx"

//string ParamID = "0x0"; // default Max parser
//string ParamID = "0x003"; //scene parser
string ParamID = "0x0001"; // DXSAS parser

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

///////PBR LIGHTING////////
struct pbrLighting {
	float3 ambientLight;
	float3 directLight;
};


pbrLighting PBRModel(vOut IN , float3 worldNormal, float4 albedo, float metalness, float roughness)
{
	worldNormal = normalize(worldNormal);
	// Outgoing light direction (vector from world-space fragment position to the "eye").
	float3 Lo = normalize(viewIMatrix[3].xyz - IN.wPos);
	
	// // Angle between surface normal and outgoing light direction.
	float cosLo = max(0.0, dot(worldNormal, Lo));

	// // Specular reflection vector.
	float3 Lr = reflect(-Lo, worldNormal);
	
	// // Fresnel reflectance at normal incidence (for metals use albedo color).
	float3 F0 = lerp(Fdielectric, albedo, metalness);

	

	// Direct lighting calculation for analytical lights.
	float3 directLighting;
	{
		float3 Li = IN.LightVector;
		float3 Lradiance = 1.0;

		// Half-vector between Li and Lo.
		float3 Lh = normalize(Li + Lo);

		// Calculate angles between surface normal and various light vectors.
		float cosLi = max(0.0, dot(worldNormal, Li));
		float cosLh = max(0.0, dot(worldNormal, Lh));

		// Calculate Fresnel term for direct lighting. 
		float3 F  = fresnelSchlick(F0, max(0.0, dot(Lh, Lo)));
		// Calculate normal distribution for specular BRDF.
		float D = ndfGGX(cosLh, roughness);
		// Calculate geometric attenuation for specular BRDF.
		float G = gaSchlickGGX(cosLi, cosLo, roughness);

		// Diffuse scattering happens due to light being refracted multiple times by a dielectric medium.
		// Metals on the other hand either reflect or absorb energy, so diffuse contribution is always zero.
		// To be energy conserving we must scale diffuse BRDF contribution based on Fresnel factor & metalness.
		float3 kd = lerp(float3(1, 1, 1) - F, float3(0, 0, 0), metalness);

		// Lambert diffuse BRDF.
		// We don't scale by 1/PI for lighting & material units to be more convenient.
		// See: https://seblagarde.wordpress.com/2012/01/08/pi-or-not-to-pi-in-game-lighting-equation/
		float3 diffuseBRDF = kd * albedo;

		// Cook-Torrance specular microfacet BRDF.
		float3 specularBRDF = (F * D * G) / max(Epsilon, 4.0 * cosLi * cosLo);

		// Total contribution for this light.
		directLighting = (diffuseBRDF + specularBRDF) * Lradiance * cosLi;
	}	
	
	// // Ambient lighting (IBL).
	float3 ambientLighting;
	{
		// Corrected to fix the difference of space signature between cubemap and 3dsMax
		float3 correctReflection = Lr.xzy* float3(-1,1,1);
		float3 correctNormal = worldNormal.xzy * float3(-1,1,1);

		// Max mip of the environment cubemap
		uint specularTextureLevels = querySpecularTextureLevels(p_radianceTex);
		// Sample last mip of the environment cubemap to get an ambient color
		float3 irradiance = p_radianceTex.Sample(wrapSampler, correctNormal, specularTextureLevels- 3).rgb;

		// // Calculate Fresnel term for ambient lighting.
		// // Since we use pre-filtered cubemap(s) and irradiance is coming from many directions
		// // use cosLo instead of angle with light's half-vector (cosLh above).
		// // See: https://seblagarde.wordpress.com/2011/08/17/hello-world/
		float3 F = fresnelSchlick(F0, cosLo);

		// // Get diffuse contribution factor (as with direct lighting).
		float3 kd = lerp(1.0 - F, 0.0, metalness);

		// // Irradiance map contains exitant radiance assuming Lambertian BRDF, no need to scale by 1/PI here either.
		float3 diffuseIBL = kd * albedo * irradiance;

		// // Sample pre-filtered specular reflection environment at correct mipmap level.
		float3 specularIrradiance = p_radianceTex.SampleLevel(wrapSampler,correctReflection, roughness * specularTextureLevels).rgb;

		// // Split-sum approximation factors for Cook-Torrance specular BRDF.
		float2 specularBRDF = p_specularBRDF_LUT.Sample(BRDFSampler, float2(cosLo, roughness)).rg;

		// // Total specular IBL contribution.
		float3 specularIBL = (F0 * specularBRDF.x + specularBRDF.y) * specularIrradiance;

		// Total ambient lighting contribution.
		ambientLighting = diffuseIBL + specularIBL;
	}	

	pbrLighting o;
	o.directLight = directLighting;
	o.ambientLight = ambientLighting;
	return o;
}

float2 transformUV(in float2 uv)
{
	uv.y += 1.f;
	uv.xy -= 0.5;
	
	float angle = p_UVRotation/360.0*3.141593*2.f;
	float2x2 rotm = {	cos(angle), -sin(angle),
						sin(angle), cos(angle)	};
	uv = mul(uv, rotm);
	
	uv.x *= p_UVTilingU;
	uv.y *= p_UVTilingV;
	uv.x -= p_UVOffsetU;
	uv.y += p_UVOffsetV;
	
	uv.xy += 0.5;

	return uv;
}

vOut VS_BASE(a2v IN)
{
	vOut OUT;
	
	OUT.UV.xy = transformUV(IN.UV);
	OUT.UV.zw = IN.UV2;
	
	//light world -> object space
	float3 lightVec = p_lightDir;
	//float3 lightVec = mul(p_lightDir, (float3x3)worldMatrix);
	lightVec = normalize(lightVec);
	
	
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

BlendState Traditional
{
	BlendEnable[0] = TRUE;
	SrcBlend[0] = SRC_ALPHA;
	DestBlend[0] = INV_SRC_ALPHA;
	BlendOp[0] = ADD;
};

//common legacy pixel shader used if no PBR viewport is enabled
#include "legacy.fx"

float4 Alpha(float4 o,vOut IN,float alphaMode)
{
    float4 color = o;
	if (alphaMode == 0)
	{
		color.a = 1;
	}
    else if (alphaMode == 1)
	{
		if (color.a <= p_alphaCutoff)
		{
		    discard;
		}
	}
	else if (alphaMode == 2 || alphaMode == 3) // Stochastic transparency for Nitrous
	{
		if (color.a <= gradientNoise((IN.Position2.xy / IN.Position2.w)*0.5*viewportSize))
		{
		    discard;
		}
	}
	return color;
}








