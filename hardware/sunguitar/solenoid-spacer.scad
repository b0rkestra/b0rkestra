
difference(){
    union(){
        translate([-14,6,-16])cube([7,12,32]);
    }

    translate([-10.5,20,11.5])rotate([90,0,0])cylinder(r=2, h=20, $fn=100);
    translate([-10.5,20,-11.5])rotate([90,0,0])cylinder(r=2, h=20, $fn=100);
}


