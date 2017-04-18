
#include <stdio.h>
#include <stdlib.h>

void Usage(char *pname);


unsigned int usize;
unsigned int usize = 0;
unsigned int ubsize = 0;
unsigned int uassoc = 0;
char urepl = 'f';
char uwalloc = 'a';
unsigned numAccesses,numMisses;


main(int argc, char *argv[])
{
  char *filename;
  int i;

  if (argc < 2) {
     Usage(argv[0]);
     exit(-1);
  }
  filename = argv[1];
  
  for (i = 2; i < argc; i++) {
     if (!strcmp(argv[i],"-l1-usize")){
        i++;
        usize = atoi(argv[i]);
     } else if (!strcmp(argv[i],"-l1-ubsize")){
        i++;
        ubsize = atoi(argv[i]);
      }
     else if (!strcmp(argv[i],"-l1-uassoc")){
        i++;
        uassoc = atoi(argv[i]);
      }
     else if (!strcmp(argv[i],"-l1-urepl")){
        i++;
        urepl = argv[i][0];
      }
     else if (!strcmp(argv[i],"-l1-uwalloc")){
        i++;
        uwalloc = argv[i][0];
      }
     else {
       printf("Ignoring urecognized option: %s\n",argv[i]);
     }
  }

  printf("Running with input: %s, l1-usize=%d,  l1-ubsize=%d,  l1-assoc=%d,  l1-repl=%c,  l1-uwalloc=%c \n",filename,usize,ubsize,uassoc,urepl,uwalloc);

  //dosim(filename,usize,ubsize,uassoc,urepl,uwalloc);
  printf ("Demand Accesses  %d\n",numAccesses);
  printf ("Demand Misses %d\n",numMisses);
  return 0;

}


void Usage(char *pname) {

  printf("Usage: %s infile <options>\n",pname);
  printf( "Options:\n");
  printf( "<-l1-usize num_bytes>    : total size in bytes\n");
  printf( "<-l1-ubsize num_bytes>   : block size in bytes\n");
  printf( "<-l1-uassoc num_levels>   : associativity level\n");
  printf( "<-l1-urepl type>         : replacement policy, 'l' - LRU, 'r'-random, 'f' fifo\n");
  printf( "<-l1-uwalloc type>      : write allocation policy, 'a' - always, 'n'-never\n");
}
