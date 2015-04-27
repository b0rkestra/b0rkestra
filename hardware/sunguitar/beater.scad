

difference(){
    sphere(r=8, center=true, $fn=200);
    translate([0,0,-6])cube([20,20,12], center=true);
    cylinder(r=1.5, h=30, center= true, $fn=100);
    translate([0,0,7])cylinder(r=3, h=10, center= true, $fn=6);
    }

