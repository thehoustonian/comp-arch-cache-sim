


public class cache_sim {
	
	private static int usize = 0;
	private static int ubsize = 0;
	private static int uassoc = 0;
	private static String urepl = "f";
	private static String uwalloc = "a";
	private static int numAccesses = 0 ,numMisses = 0;


	public static void main (String[] args) {
	
				
		if (args.length < 2) {
			System.out.println("Usage: cache_sim infile <options>");
			System.out.println("Options:");
			System.out.println("<-l1-usize num_bytes>    : total size in bytes");
			System.out.println("<-l1-ubsize num_bytes>   : block size in bytes");
			System.out.println("<-l1-uassoc num_levels>   : associativity level");
			System.out.println("<-l1-urepl type>         : replacement policy, 'l' - LRU, 'r'-random, 'f' fifo");
			System.out.println("<-l1-uwalloc type>      : write allocation policy, 'a' - always, 'n'-never");
			System.exit(-1);
		
		}
		int i;
		i = 1;
		while (i < args.length) {
			if (args[i].equals("-l1-usize")) {
				i += 1;
				usize = Integer.parseInt(args[i]);
			}
			else if (args[i].equals("-l1-ubsize")){
				i += 1;
				ubsize = Integer.parseInt(args[i]);
			}
			else if (args[i].equals("-l1-uassoc")){
				i += 1;
				uassoc = Integer.parseInt(args[i]);
			}
			else if (args[i].equals("-l1-urepl")){
				i += 1;
				urepl = args[i];
			}
			else if (args[i].equals("-l1-uwalloc")){
				i += 1;
				uwalloc = args[i];
				}
			else {
				System.out.println("Ignoring unrecognized option: " + args[i]);
				}
        
			i += 1;
		}
		
		String fname = args[0];
		
		String s = String.format("Running with input: %s, l1-usize=%d,  l1-ubsize=%d,  l1-assoc=%d,  l1-repl=%s,  l1-uwalloc=%s \n",fname,usize,ubsize,uassoc,urepl,uwalloc);
		System.out.println(s);
	
		//do the simulation
		
		//print results
		System.out.println(String.format("Demand Accesses %d",numAccesses));
		System.out.println(String.format("Demand Misses %d",numMisses));
		
	}

}

	