

difference(){
    linear_extrude(height = 8, center = true, convexity = 10, $fn=200)
        import (file = "solenoid-clamp.dxf", layer = "base");
    translate([88,0,0])rotate([90,0,0])cylinder(r=2, h=20, $fn=100);
    translate([-88,0,0])rotate([90,0,0])cylinder(r=2, h=20, $fn=100);
    
}
