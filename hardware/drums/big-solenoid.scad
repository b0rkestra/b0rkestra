module solenoid(){
	cylinder(r= 58/2, h =100, center=true);
	translate([0,0,50])cylinder(r= 64/2, h =5, center=true);
	translate([0,0,50])cylinder(r= 35/2, h =100, center=true);
	translate([0,72.5/2,45])cylinder(r= 6/2, h =20, center=true);
	translate([0,-72.5/2,45])cylinder(r= 6/2, h =20, center=true);
}
module support(){
	difference() {
		union() {
			translate([-0,0,15.5])cube([65,20,5], center = true);
			
			translate([-33,7.5,20.5])cube([35,5,15], center = true);
			translate([-50,7.5,20.5])rotate([90,0,0])cylinder(h=5,r=7.5 , center=true, $fn=100);

			translate([-33,-7.5,20.5])cube([35,5,15], center = true);
			translate([-50,-7.5,20.5])rotate([90,0,0])cylinder(h=5,r=7.5 , center=true, $fn=100);

			translate([-23,0,20.5])cube([20,20,15], center = true);

			translate([74.4/2-2.5,0,20.5])cube([5,20,15], center = true);

		}	
		
		/*translate([54.4/2-10,13/2,10])cylinder(h=20,r=1.5, center=true, $fn=100);
		translate([54.4/2-30,13/2,10])cylinder(h=20,r=1.5, center=true, $fn=100);
		translate([54.4/2-10,-13/2,10])cylinder(h=20,r=1.5, center=true, $fn=100);
		translate([54.4/2-30,-13/2,10])cylinder(h=20,r=1.5, center=true, $fn=100);
		translate([29/2-5.5,13/2,10])cylinder(h=20,r=1, center=true, $fn=100);
		translate([-29/2+5.5,-13/2,10])cylinder(h=20,r=1, center=true, $fn=100);*/

		translate([25,6,10])cylinder(h=20,r=1.5, center=true, $fn=100);
		translate([25,-6,10])cylinder(h=20,r=1.5, center=true, $fn=100);
		translate([15,6,10])cylinder(h=20,r=1.5, center=true, $fn=100);
		translate([15,-6,10])cylinder(h=20,r=1.5, center=true, $fn=100);

		translate([-50,0,20])rotate([90,0,0])cylinder(h=30,r=3 , center=true, $fn=100);
		translate([-10.5,0,38])rotate([90,0,0])cylinder(h=21,r=20 , center=true, $fn=400);

	}
	difference() {
		//translate([54.4/2-8,0,24])rotate([90,90,0])cylinder(h=21,r=2 , center=true, $fn=200);
		union(){
			translate([0,0,20.5])cube([65,5,15], center = true);
			translate([24.5,0,26])rotate([90,0,0])cylinder(r=8, h=5, center=true, $fn=200);
		}
		translate([24.5,0,26])rotate([90,0,0])cylinder(r=3, h=10, center=true, $fn=200);

	}

}

module bearing() {
	difference() {
		cylinder(h=6,r=19/2 , center=true, $fn=100);
		cylinder(h=7,r=6/2 , center=true, $fn=100);
	}
}

module arm() {
	difference() {
		union() {
			translate([-61,0,30])cube([8,5.5,80], center = true);
			translate([-50,0,20])rotate([90,0,0])cylinder(h=5.5,r=15 , center=true, $fn=100);
			
			translate([-57,0,-10])rotate([90,0,0])cylinder(h=5.5,r=8 , center=true, $fn=100);

		}
		translate([-50,0,20])rotate([90,0,0])color([0.5,0.5,0.5])cylinder(h=6,r=19/2 , center=true, $fn=100);

		translate([-60,0,0])rotate([0,90,0])cylinder(h=50,r=1.5 , center=true, $fn=100);
		translate([-60,0,60])rotate([0,90,0])cylinder(h=50,r=1.5 , center=true, $fn=100);

		translate([-62,0,65])rotate([90,0,0])cylinder(h=20,r=1.5 , center=true, $fn=100);
		translate([-62,0,-5])rotate([90,0,0])cylinder(h=20,r=1.5 , center=true, $fn=100);
		translate([-62,0,5])rotate([90,0,0])cylinder(h=20,r=1.5 , center=true, $fn=100);

		translate([-57,0,-10])rotate([90,0,0])cylinder(h=6.5,r=3 , center=true, $fn=100);

	}
}


module holder(){
	difference() {
		translate([-70,0,30])cube([10,20,80], center = true);
		translate([-76,0,30])rotate([0,0,45])cube([10,10,81], center = true);	
		translate([-60,0,0])rotate([0,90,0])cylinder(h=50,r=1.5 , center=true, $fn=100);
		translate([-60,0,60])rotate([0,90,0])cylinder(h=50,r=1.5 , center=true, $fn=100);

		translate([-73,0,0])rotate([0,90,0])cylinder(h=10,r=3 , center=true, $fn=100);
		translate([-73,0,60])rotate([0,90,0])cylinder(h=10,r=3 , center=true, $fn=100);
		translate([-65.5,0,-5])cube([2,21,5], center = true);
		translate([-65.5,0,65])cube([2,21,5], center = true);
	}		
}


module bracket() {

	difference(){
	intersection(){
		rotate([0,0,90])translate([0,0,13])linear_extrude(height = 26, center = true, convexity = 10)
			import (file = "big-solenoid-base.dxf", layer = "base", $fn=200);
		rotate([0,90,90])linear_extrude(height = 200, center = true, convexity = 10)
			import (file = "big-solenoid-base.dxf", layer = "profile", $fn=200);
		rotate([90,0,90])linear_extrude(height = 100, center = true, convexity = 10)
			import (file = "big-solenoid-base.dxf", layer = "profile2", $fn=200);
	}
	
	translate([0,6,12])rotate([0,90,0])cylinder(r=1.5, h=100, center=true, $fn=100);
	translate([0,-6,12])rotate([0,90,0])cylinder(r=1.5, h=100, center=true, $fn=100);
	translate([0,6,22])rotate([0,90,0])cylinder(r=1.5, h=100, center=true, $fn=100);
	translate([0,-6,22])rotate([0,90,0])cylinder(r=1.5, h=100, center=true, $fn=100);
	
	translate([-22,6,12])rotate([0,90,0])cylinder(r=2.5, h=10, center=true, $fn=100);
	translate([-22,-6,12])rotate([0,90,0])cylinder(r=2.5, h=10, center=true, $fn=100);
	translate([-25,6,22])rotate([0,90,0])cylinder(r=2.5, h=10, center=true, $fn=100);
	translate([-25,-6,22])rotate([0,90,0])cylinder(r=2.5, h=10, center=true, $fn=100);

	
	}
	


	/*
	*/

	/*difference(){
		union(){
			cylinder(r = 43, h=6);
		}	
		translate([0,0,1])cylinder(r= 40/2, h =12, center=true);

		translate([0,72.5/2,0])cylinder(r= 6.5/2, h =20, center=true);
		translate([0,-72.5/2,0])cylinder(r= 6.5/2, h =20, center=true);
			translate([6,-50,-2])cube([50,100,10]);

	}*/
	
}

module armature_stopper(){
	difference(){
		union(){
			cylinder(r=17, h=6, center=true, $fn=200);
			translate([0,72.5/2,-2])cylinder(r= 15/2, h =10, center=true, $fn=200);
			translate([0,-72.5/2,-2])cylinder(r= 15/2, h =10, center=true, $fn=200);
			cube([15,75,6], center = true, $fn=200);
		}

		cylinder(r=10, h=20, center=true, $fn=200);
		translate([0,72.5/2,0])cylinder(r= 6.1/2, h =20, center=true, $fn=200);
		translate([0,-72.5/2,0])cylinder(r= 6.1/2, h =20, center=true, $fn=200);	
	}
	

	

}

//support();
//solenoid();
translate([0,0,110])armature_stopper();
//arm();
//holder();
//translate([0,0,52.5])color([0.4,0.4,0.1])bracket();

