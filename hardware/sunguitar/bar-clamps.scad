union(){
    difference(){
        linear_extrude(height = 7, center = true, convexity = 10, $fn=200)
            import (file = "bar-clamps.dxf", layer = "base");

        translate([-11.5,-4,0])rotate([90,0,0])cylinder(r=1.5, h=10, $fn=100);
        translate([15.5,-4,0])rotate([90,0,0])cylinder(r=1.5, h=10, $fn=100);
        translate([-11.5,2,0])rotate([90,0,0])cylinder(r=3, h=10, $fn=100);
        translate([15.5,2,0])rotate([90,0,0])cylinder(r=3, h=10, $fn=100);
        //translate([9.5,8,0])rotate([90,0,0])cylinder(r=1, h=20, $fn=100);
    }

    translate([0,0,-4])linear_extrude(height = 1, center = true, convexity = 10, $fn=200)
        import (file = "bar-clamps.dxf", layer = "blank");    
}
