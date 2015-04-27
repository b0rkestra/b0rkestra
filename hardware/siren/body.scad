module armature8(){
    difference(){
        union(){
            translate([0,0,-6])cylinder(r=25, h=2.5, $fn=200);
            translate([0,0,1.5])linear_extrude(height = 15, center = true, convexity = 10, $fn=200)
                import (file = "Vanes.dxf", layer = "vane-8");
            translate([0,0,-5])cylinder(r=3, h=5, $fn=200);
        }
        translate([0,0,-7])cylinder(r=1, h=20, $fn=200);
    }
}

module stator8(){
    difference(){
        union(){
            translate([0,0,-3])cylinder(r=30, h=4, $fn=200);
            translate([0,0,10])linear_extrude(height = 18, center = true, convexity = 10, $fn=200)
                import (file = "Vanes.dxf", layer = "stator-8");

        }

        translate([0,0,-1.05])cylinder(r=19, h=2.1, $fn=200);
        translate([0,0,-3.05])cylinder(r=21, h=2.1, $fn=200);

        for(i=[0:7])
            rotate([0,0,i*(45)-12.5])translate([28,0,-9])cylinder(r=1.25,h=30, $fn=100);

    }
}


module base(){
    difference(){
        union(){
            translate([0,0,-6])cylinder(r=30, h=2, $fn=200);
            translate([0,0,-9])cylinder(r=15, h=3, $fn=200);

        }
        translate([0,0,-14])cylinder(r=6, h=20, $fn=200);

        translate([16.5/2,0,-14])cylinder(r=1, h=20, $fn=200);
        translate([-16.5/2,0,-14])cylinder(r=1, h=20, $fn=200);
        translate([16.5/2,0,-5.5])cylinder(r=2.5, h=2, $fn=200);
        translate([-16.5/2,0,-5.5])cylinder(r=2.5, h=2, $fn=200);
        

        for(i=[0:7])
            rotate([0,0,i*(45)+22.5])translate([28,0,-10])cylinder(r=1.25,h=20, $fn=100);
    }
}


module tube(){
    translate([0,0,-30])difference(){
        cylinder(r=41/2, h=60, center = true, $fn=200);
        cylinder(r=38/2, h=61, center = true, $fn=200);
    }
}


module servomount(){
    translate([0,0,-30]){
        difference(){
            union(){
                cylinder(r=45/2, h=3, center = true, $fn=200);
                translate([23.5,0,0])cube([10,5,3], center=true);
            }
            cylinder(r=41.5/2, h=4, center = true, $fn=200);
            translate([27,10,0])rotate([90,0,0])cylinder(r=0.75, h=20, $fn=200);

        }
    }
}

module flapclamp(){
 translate([0,0,-30]){
        difference(){
            union(){
                cylinder(r=45/2, h=5, center = true, $fn=200);
                translate([23.5,0,0])cube([13,10,5], center=true);
            }
            cylinder(r=41.5/2, h=6, center = true, $fn=200);
            translate([28,-3,-10])rotate([0,0,0])cylinder(r=0.75, h=20, $fn=200);
            translate([28,3,-10])rotate([0,0,0])cylinder(r=0.75, h=20, $fn=200);

        }

    }   
}


module servoarm(){
    difference(){
        union(){
            cylinder(r=9/2, h=5, $fn=100);
            translate([0,15,2.5])cylinder(r=3, h=2.5, $fn=100);
            translate([-3,0,2.5])cube([6,15,2.5]);
        }
        translate([0,0,-0.01])cylinder(r=3.75/2, h=2.5, $fn=100);        
        translate([0,15,2.49])cylinder(r=1, h=3, $fn=100);
        translate([0,11,2.49])cylinder(r=1, h=3, $fn=100);
        translate([0,7,2.49])cylinder(r=1, h=3, $fn=100);

    }

}

//translate([35,5,-30])rotate([270,-90,0])servoarm();
//translate([0,0,-10])servomount();
//translate([0,0,15])servomount();
//translate([0,0,-28.5])rotate([0,0,180])flapclamp();
//tube();
//stator8();    
//translate([0,0,12])rotate([180,0,0])armature8();
translate([0,0,16])rotate([180,0,10])base();

