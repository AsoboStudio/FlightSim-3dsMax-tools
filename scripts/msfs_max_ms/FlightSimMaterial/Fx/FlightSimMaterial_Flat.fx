#include "core.fx"



float4 PS_ENVOCCLUDER(vOut IN) : SV_Target
{
	float4 o = Alpha(float4(0,1,0,0.02),IN, 2);
    return o;
}

float4 PS_INVISIBLE(vOut IN) : SV_Target
{
    float4 o = Alpha(float4(1,0,0,0.02),IN,2);
	return o;
}

////////TECHNIQUES////////
//Group: https://msdn.microsoft.com/en-us/library/windows/desktop/ff476120(v=vs.85).aspx
//Technique: https://msdn.microsoft.com/en-us/library/windows/desktop/ff476122(v=vs.85).aspx
//State Groups: https://msdn.microsoft.com/en-us/library/windows/desktop/ff476121(v=vs.85).aspx

technique11 Tech_EnvOccluder
{
	pass p0
	{
        SetVertexShader(CompileShader(vs_5_0,VS_BASE()));
        SetGeometryShader( NULL );
		SetPixelShader(CompileShader(ps_5_0,PS_ENVOCCLUDER()));
	}
}

technique11 Tech_Invisible
{
	pass p0
	{
        SetVertexShader(CompileShader(vs_5_0,VS_BASE()));
        SetGeometryShader( NULL );
		SetPixelShader(CompileShader(ps_5_0,PS_INVISIBLE()));
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



