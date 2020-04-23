--simple utility to plot animation of selected object
-- tested with Constraint animation

disableSceneRedraw()
for obj in selection do (
    tmp = Point()
    --store anim to a point
    for t = animationRange.start to animationRange.end do (
        if redrawFlag do sliderTime = t -- update
        with animate on at time t tmp.transform = obj.transform
    )

    --remove constraint on original object
    obj.pos.controller = Position_XYZ ()
    obj.rotation.controller = Euler_XYZ ()
    obj.transform = tmp.transform

    --copy back anim from point
    for t = animationRange.start to animationRange.end do (
        if redrawFlag do sliderTime = t -- update
        with animate on at time t obj.transform = tmp.transform
    )
    delete tmp
)
enableSceneRedraw()
