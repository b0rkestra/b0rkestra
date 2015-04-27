
module solenoid(){
	difference() {
		union(){
			cube([54.4,20,26], center = true);
			translate([-54.4/2-5,0,0])cube([10,10,10], center = true);	
		}

		translate([54.4/2-10,13/2,10])cylinder(h=20,r=1, center=true, $fn=100);
		translate([54.4/2-30,13/2,10])cylinder(h=20,r=1, center=true, $fn=100);
		translate([54.4/2-10,-13/2,10])cylinder(h=20,r=1, center=true, $fn=100);
		translate([54.4/2-30,-13/2,10])cylinder(h=20,r=1, center=true, $fn=100);
	}	
}


module solenoid_ebay(){
	difference() {
		union(){
			cube([29,21,24], center = true);
			translate([-29/2-5,0,0])cube([10,10,10], center = true);	
			translate([29/2+5,0,0])cube([10,10,10], center = true);	
		}

		//translate([54.4/2-10,13/2,10])cylinder(h=20,r=1, center=true, $fn=100);
		//translate([54.4/2-30,13/2,10])cylinder(h=20,r=1, center=true, $fn=100);
		

		translate([29/2-5.5,21/2-3.75,10])cylinder(h=20,r=1, center=true, $fn=100);
		translate([-29/2+5.5,-21/2+3.75,10])cylinder(h=20,r=1, center=true, $fn=100);
	}	
}

module support(){
	difference() {
		union() {
			translate([-2.8,0,15.5])cube([60,20,5], center = true);
			
			translate([-33,7.5,20.5])cube([35,5,15], center = true);
			translate([-50,7.5,20.5])rotate([90,0,0])cylinder(h=5,r=7.5 , center=true, $fn=100);

			translate([-33,-7.5,20.5])cube([35,5,15], center = true);
			translate([-50,-7.5,20.5])rotate([90,0,0])cylinder(h=5,r=7.5 , center=true, $fn=100);

			translate([-23,0,20.5])cube([20,20,15], center = true);

			translate([54.4/2-2.5,0,20.5])cube([5,20,15], center = true);

		}	
		
		/*translate([54.4/2-10,13/2,10])cylinder(h=20,r=1.5, center=true, $fn=100);
		translate([54.4/2-30,13/2,10])cylinder(h=20,r=1.5, center=true, $fn=100);
		translate([54.4/2-10,-13/2,10])cylinder(h=20,r=1.5, center=true, $fn=100);
		translate([54.4/2-30,-13/2,10])cylinder(h=20,r=1.5, center=true, $fn=100);
		translate([29/2-5.5,13/2,10])cylinder(h=20,r=1, center=true, $fn=100);
		translate([-29/2+5.5,-13/2,10])cylinder(h=20,r=1, center=true, $fn=100);*/

		translate([29/2-5.5 - 2,21/2-3.75,10])cylinder(h=20,r=1, center=true, $fn=100);
		translate([-29/2+5.5 - 2,-21/2+3.75,10])cylinder(h=20,r=1, center=true, $fn=100);

		translate([-50,0,20])rotate([90,0,0])cylinder(h=30,r=3 , center=true, $fn=100);
		translate([-10.5,0,38])rotate([90,0,0])cylinder(h=21,r=20 , center=true, $fn=400);

	}
	difference() {
		translate([-5,0,20.5])cube([55,5,15], center = true);
		translate([54.4/2-8,0,24])rotate([90,90,0])cylinder(h=21,r=2 , center=true, $fn=200);
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
			translate([-61,0,20])cube([8,5.5,60], center = true);
			translate([-50,0,20])rotate([90,0,0])cylinder(h=5.5,r=15 , center=true, $fn=100);
		}
		translate([-50,0,20])rotate([90,0,0])color([0.5,0.5,0.5])cylinder(h=6,r=19/2 , center=true, $fn=100);

		translate([-60,0,0])rotate([0,90,0])cylinder(h=50,r=1.5 , center=true, $fn=100);
		translate([-60,0,40])rotate([0,90,0])cylinder(h=50,r=1.5 , center=true, $fn=100);

		translate([-62,0,45])rotate([90,0,0])cylinder(h=20,r=1.5 , center=true, $fn=100);
		translate([-62,0,-5])rotate([90,0,0])cylinder(h=20,r=1.5 , center=true, $fn=100);
		translate([-62,0,5])rotate([90,0,0])cylinder(h=20,r=1.5 , center=true, $fn=100);
	}
}


module holder(){
	difference() {
		translate([-70,0,20])cube([10,20,60], center = true);
		translate([-76,0,20])rotate([0,0,45])cube([10,10,61], center = true);	
		translate([-60,0,0])rotate([0,90,0])cylinder(h=50,r=1.5 , center=true, $fn=100);
		translate([-60,0,40])rotate([0,90,0])cylinder(h=50,r=1.5 , center=true, $fn=100);

		translate([-73,0,0])rotate([0,90,0])cylinder(h=10,r=3 , center=true, $fn=100);
		translate([-73,0,40])rotate([0,90,0])cylinder(h=10,r=3 , center=true, $fn=100);
		translate([-65.5,0,-5])cube([2,21,5], center = true);
		translate([-65.5,0,45])cube([2,21,5], center = true);
	}		
}


module pull_arm(){
	
	difference(){
		union(){
			cube([28,8,4], center=true);
			translate([17-3.5,0,0])cylinder(r=4, h=4, center=true, $fn=100);
			translate([-17+3.5,0,0])cylinder(r=4, h=4, center=true, $fn=100);	
		}
		

		cylinder(r=1.5, h=10, center=true, $fn=100);
		translate([17-3.5,0,0])cylinder(r=1, h=10, center=true, $fn=100);
		translate([-17+3.5,0,0])cylinder(r=1, h=10, center=true, $fn=100);	
	}
	
}

//pull_arm();


//color([0.4,0.4,0.8])solenoid();
//translate([-2,0,0])solenoid_ebay();
//support();
//translate([-50,0,20])rotate([90,0,0])color([0.5,0.5,0.5])bearing();
//holder();
arm();