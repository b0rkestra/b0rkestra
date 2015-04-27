module speaker_cap(){
    difference(){
        translate([0,0,-2])cylinder(h=16, r=44/2, center=true, $fn=200);
        translate([0,0,8])cylinder(h=10, r=40.5/2, center=true, $fn=200);
        translate([0,0,1.1])cylinder(h=4, r1=36/2,r2=39.5/2, center=true, $fn=200);

        translate([0,0,-11])cylinder(h=10, r=41.5/2, center=true, $fn=200);
        translate([0,0,0])cylinder(h=40, r=36/2, center=true, $fn=200);    
        translate([0,0,-10])rotate([90,0,0])cylinder(h=60, r=12,center=true, $fn=200);
    translate([0,0,-10])rotate([90,0,90])cylinder(h=60, r=12,center=true, $fn=200);
    }
}

translate([00,0,0])speaker_cap();
translate([50,0,0])speaker_cap();
translate([100,0,0])speaker_cap();
translate([00,50,0])speaker_cap();
translate([50,50,0])speaker_cap();
translate([100,50,0])speaker_cap();
translate([00,100,0])speaker_cap();
translate([50,100,0])speaker_cap();
translate([100,100,0])speaker_cap();
translate([00,150,0])speaker_cap();
translate([50,150,0])speaker_cap();
translate([100,150,0])speaker_cap();

