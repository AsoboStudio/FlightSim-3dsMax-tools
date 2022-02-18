static const float PI = 3.141592;

///////FUNCTIONS//////
float linearstep( float lo, float hi, float input )
{
	return saturate( (input-lo) / (hi-lo) );
}

float gradientNoise(float2 pixelPos)
{
	return frac( 52.9829189f * frac( dot( pixelPos, float2(0.06711056f,0.00583715f) ) ) );
}

float median(float3 v)
{
    return max(min(v.x, v.y), min(max(v.x, v.y), v.z));
}

float2 Rotate2D(float2 vecToRotate, float cosOfAngle, float sinOfAngle)
{
	return float2(dot(vecToRotate, float2(cosOfAngle, sinOfAngle)), dot(vecToRotate, float2(-sinOfAngle, cosOfAngle)));
}

//// RGB HSV Color Space Transformation
//static const float Epsilon = 0.0000000001;
//
float3 RGBtoHCV(float3 RGB)
{
    float4 P = lerp(float4(RGB.bg, -1.0, 2.0 / 3.0), float4(RGB.gb, 0.0, -1.0 / 3.0), step(RGB.b, RGB.g));
    float4 Q = lerp(float4(P.xyw, RGB.r), float4(RGB.r, P.yzx), step(P.x, RGB.r));
    float C = Q.x - min(Q.w, Q.y);
    float H = abs((Q.w - Q.y) / (6 * C + Epsilon) + Q.z);
    return float3(H, C, Q.x);
}
float3 HUEtoRGB(float H)
{
    float R = abs(H * 6 - 3) - 1;
    float G = 2 - abs(H * 6 - 2);
    float B = 2 - abs(H * 6 - 4);
    return saturate(float3(R, G, B));
}
float3 HSVtoRGB(float3 HSV)
{
    float3 RGB = HUEtoRGB(HSV.x);
    return ((RGB - 1) * HSV.y + 1) * HSV.z;
}
float3 RGBtoHSV(float3 RGB)
{
    float3 HCV = RGBtoHCV(RGB);
    float S = HCV.y / (HCV.z + Epsilon);
    return float3(HCV.x, S, HCV.z);
}

// -----------------------------------------------
// YUV color space

// RGB -> YUV matrix
static const float3x3 RGB_TO_YUV =
{
	{ +0.21260, +0.71520, +0.07220 }, // LUMINANCE_VECTOR_BT_709
	{ -0.09991, -0.33609, +0.43600 },
	{ +0.61500, -0.55861, -0.05639 }
};

// YUV -> RGB matrix
static const float3x3 YUV_TO_RGB =
{
	{ +1.00, +0.00000, +1.28033 },
	{ +1.00, -0.21482, -0.38059 },
	{ +1.00, +2.12798, +0.00000 }
};

// RGB -> YUV
float3 RGBToYUV(float3 RGB)
{
	return mul(RGB_TO_YUV, RGB);
}

// YUV -> RGB
float3 YUVToRGB(float3 YUV)
{
	return mul(YUV_TO_RGB, YUV);
}

// GGX/Towbridge-Reitz normal distribution function.
// Uses Disney's reparametrization of alpha = roughness^2.
float ndfGGX(float cosLh, float roughness)
{
	float alpha   = roughness * roughness;
	float alphaSq = alpha * alpha;

	float denom = (cosLh * cosLh) * (alphaSq - 1.0) + 1.0;
	return alphaSq / (PI * denom * denom);
}

// Single term for separable Schlick-GGX below.
float gaSchlickG1(float cosTheta, float k)
{
	return cosTheta / (cosTheta * (1.0 - k) + k);
}

// Schlick-GGX approximation of geometric attenuation function using Smith's method.
float gaSchlickGGX(float cosLi, float cosLo, float roughness)
{
	float r = roughness + 1.0;
	float k = (r * r) / 8.0; // Epic suggests using this roughness remapping for analytic lights.
	return gaSchlickG1(cosLi, k) * gaSchlickG1(cosLo, k);
}

// Shlick's approximation of the Fresnel factor.
float3 fresnelSchlick(float3 F0, float cosTheta)
{
	return F0 + (1.0 - F0) * pow(1.0 - cosTheta, 5.0);
}

// Returns number of mipmap levels for specular IBL environment map.
uint querySpecularTextureLevels(TextureCube <float4> radianceMap)
{
	uint width, height, levels;
	radianceMap.GetDimensions(0, width, height, levels);
	return levels;
}

float3 GetWorldNormal(float3 worldTangent, float3 worldBinormal, float3 worldNormal , float3 tangentNormal )
{
	float3x3 TBN = float3x3(normalize(worldTangent), normalize(worldBinormal),normalize(worldNormal)); //transforms world=>tangent space
	TBN = transpose(TBN);	
	
	float3 wNormal = mul(TBN, normalize(tangentNormal)); //N
	wNormal = float3(wNormal.x,wNormal.y,wNormal.z);
	return wNormal;
}

float randomValue(float2 p)
{
	p += float2(0, 12545.54);
	p = frac(p*0.3183099 + .1);
	p *= 17.0;
	return frac(p.x*p.y*(p.x + p.y));
}