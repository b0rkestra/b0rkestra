
difference(){
    union(){
        cylinder(r=7, h=15, $fn=100, center=true);
        translate([-7,0,-7.5])cube([11,14,15]); 
        translate([-14,6,-16])cube([7,8,32]);
    }

    translate([0,-1,-8])cube([0.5,20,16]);
    cylinder(r=4.1, h=20, $fn=100, center=true);
    translate([-10,10,0])rotate([0,90,0])cylinder(r=2, h=20, $fn=100);
    translate([-10.5,20,11.5])rotate([90,0,0])cylinder(r=2, h=20, $fn=100);
    translate([-10.5,20,-11.5])rotate([90,0,0])cylinder(r=2, h=20, $fn=100);
}


