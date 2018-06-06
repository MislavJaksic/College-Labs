// 20b-inc-dec-atomic-ltl.pml
int x = 0;
bool doneinc = false;
bool donedec = false;

proctype inc(){
	 int tmp;
	 atomic {tmp = x;
	 x = tmp + 1; }
	 doneinc = true;
}

proctype dec(){
	 int tmp;
	 atomic {tmp = x;
	 x = tmp - 1;}
	 donedec = true;
}

init {
 	run inc();
 	run dec();
}      

ltl finallyzero {
     always ((!(doneinc && donedec)) || x == 0);
}

