module head_and_handle(){
	cylinder(r=2, h=100, center=true, $fn=40);
	translate([0,0,50+2])rotate([90,0,0])cylinder(r=2.4, h=40, center=true, $fn=40);
}

module cross_bar(){
	translate([0,5,-20])rotate([90,0,90])cylinder(r=2, h=200, center=true, $fn=30);
}

module t_connector(){
	difference(){
		translate([0,0,51])cube([7,10,10], center=true);
		translate([0,6,46])rotate([0,90,0])cylinder(r=3.5,h=10, center=true, $fn=100);
		translate([0,-6,46])rotate([0,90,0])cylinder(r=3.5,h=10, center=true, $fn=100);
		head_and_handle();	
	}	
}


module pivot(){
	difference(){
		union(){
			translate([0,1,-20])cube([6,8.5,10], center=true);
			translate([0,5,-20])rotate([90,0,90])cylinder(r=5,h=6, center=true);
		}
		head_and_handle();	
		cross_bar();
	}
}


module pad(){
	difference(){

	union(){

	translate([0,3,-44])cube([10,4,10], center=true);
	translate([0,0,-44])cylinder(h=10, r=4, center=true);
	}
	head_and_handle();
	}


}

module hammer(){
	head_and_handle();	
	t_connector();
	pivot();
	pad();
}

module hammers(){
	 for(d = [-50 : 20 : 50]){
	 	translate([d,0,0])hammer();
	 }
}

//pivot();
pad();
//hammers();
//cross_bar();
//t_connector();