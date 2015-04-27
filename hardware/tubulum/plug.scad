module tube(){
    translate([0,0,-30])difference(){
        cylinder(r=41/2, h=100, center = true, $fn=200);
        cylinder(r=38/2, h=101, center = true, $fn=200);

        translate([0,10,40])difference(){
            translate([0,40,-40])rotate([45,0,0])cube([41,40,100], center = true);
            translate([0,10,1.4])cube([42,60,40], center = true);    
        }
    }
}



module plug(){
    difference(){
        cylinder(r=37.8/2, h=15, center = true, $fn=200);
        translate([35,0,0])cube([40,40,40], center = true);    
    }
}



//tube();
plug();
