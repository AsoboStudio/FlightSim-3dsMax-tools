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

uniform bool p_corridorEnabled <
	string UIName = "p_corridorEnabled";
	> = false;


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
TextureCube <float4> p_irradianceTex<
	string UIName = "p_irradianceTex";
	>;
TextureCube <float4> p_radianceTex<
	string UIName = "p_radianceTex";
	>;
Texture2D <float4> p_specularBRDF_LUT <
	string UIName = "p_specularBRDF_LUT ";
	>;


////////CONSTANTES////////
cbuffer UpdatePerFrame : register(b0)
{
float4x4 worldMatrix 			: World;
float4x4 viewMatrix				: View;
float4x4 projMatrix 			: Projection;
float4x4 worldViewProjMatrix 	: WorldViewProj;
float4x4 worldIMatrix 			: WorldI;
float4x4 WorldITXf				: WorldInverseTranspose;
float4x4 viewIMatrix 			: ViewI;
float4x4 viewInverseMatrix		: ViewInverse;
}

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


////////////SAMPLER///////////
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

SamplerState BRDFSampler
{
	FILTER = ANISOTROPIC;
	MaxAnisotropy = 8;
	AddressU = CLAMP;
	AddressV = CLAMP;
};