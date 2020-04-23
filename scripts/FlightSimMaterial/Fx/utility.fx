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