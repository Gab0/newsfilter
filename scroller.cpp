#include <stdio.h>
#include <cstdlib>
#include <string.h>
#include <unistd.h>
#include <locale.h>

#include <codecvt>


#include <iostream>
#include <locale>
#include <fstream>
#include <string>
#include <iterator>
#define bad(x) (aStr[x] < 0)
std::string GetStdoutFromCommand(std::string cmd);
void renewMessage(char *alloc);
int getpid(char *PID, char *procname);
std::string utf8substr(std::string originalString, int SubStrStart, int SubStrLength);

#define min(a,b)                                \
  ({ __typeof__ (a) _a = (a);                   \
    __typeof__ (b) _b = (b);                    \
    _a < _b ? _a : _b; })


int main(int argc, char **argv)
{

  setlocale(LC_ALL, "");
  int STEP= 1;
  float SLEEPTIME = 0.5;
  //FILE *origin = fopen ("~/.scroll", "r");

  char *StatusBarPID = (char *)malloc(100 * sizeof(char));

  char *outpath = (char *)malloc(100 * sizeof(char));
  printf("Writing to %s.\n", outpath);

  char message[6000];
  //char submessage[150];

  char *submessage = (char *)malloc(150 * sizeof(char));
  char *outputprocname = (char *)malloc(16 * sizeof(char));
  if (argc > 1)
    outputprocname = argv[1];
  else
    memcpy(outputprocname, "xmobar", 7);

  printf("Getting PID of %s\n", outputprocname);

  if (getpid(StatusBarPID, outputprocname))
    return 1;

  printf("Endpoint PID %s\n", StatusBarPID);
  asprintf(&outpath, "/proc/%s/fd/0", StatusBarPID);

  FILE *output = fopen( outpath, "a" );
  //std::string P(outpath);
  //std::ofstream Output;
  //Output.open(P);

  int commresult =0;
  int horizontalspan = 116;
  printf("Writing to %s\n", outpath);
  int effectivespan = 0;
  int initPoint=0;

  std::string Text;
  std::string OutputText;
  std::wstring_convert<std::codecvt_utf8_utf16<char16_t>, char16_t> utf16conv;
  for (;;)
    {
      if (initPoint < Text.length())
    {
      //while(message[initPoint] > 127)//because of bugz;
      //  initPoint++;
      printf("loop %i. TL=%i\n", initPoint, Text.length());
      effectivespan=min(horizontalspan, strlen(message)-initPoint-1) ;

      //strncpy( submessage, &message[initPoint+1], effectivespan);
      //OutputText = Text.substr(initPoint, effectivespan);
      OutputText = utf8substr(Text, initPoint, effectivespan);
      OutputText += "\n";


      std::fprintf(output, "%s", OutputText.c_str());
      std::cout << OutputText;

      if (commresult<0)
        return 1;
      fflush(output);

      printf("Success %i\n\n", commresult);

      usleep((int)(SLEEPTIME * 1000000));
      initPoint+=STEP;
    }
    else
      {
        //renewMessage(message);
        Text=GetStdoutFromCommand("python newsfilter.py");


        //std::printf("NN%s\n\n", Text_.c_str());
        initPoint=0;
      }
    }
  return 0;
}

std::string utf8substr(std::string originalString, int SubStrStart, int SubStrLength)
{
  int len = 0, byteIndex = 0;
  const char* aStr = originalString.c_str();
  size_t origSize = originalString.size();

  int SubStrEnd = SubStrStart + SubStrLength-1;
  int endcut=0, startcut=0;


  // START-POINT-TRIM;
  printf( "Before Start %i\n", aStr[SubStrStart-1]  );
  printf( "On Start %i\n", aStr[SubStrStart] );
  printf( "After Start %i\n", aStr[SubStrStart+1] );
  printf( "Two After Start %i\n\n", aStr[SubStrStart+2 ]);
  if bad(SubStrStart-1)
          {
            while bad(SubStrStart+startcut)
                       startcut+=1;

          }

  // END-POINT-TRIM;
  printf( "Before End %i\n", aStr[SubStrEnd-1]  );
  printf( "On End  %i\n", aStr[SubStrEnd]);
  printf( "After End %i\n", aStr[SubStrEnd+1]);
  if bad(SubStrEnd+1)
          {

            while bad(SubStrEnd-endcut)
                       endcut--;


            SubStrLength-=endcut;
          }
  printf("%i;%i\n", startcut,endcut);
  std:: string csSubstring= originalString.substr(SubStrStart, SubStrLength);
  csSubstring.replace(0,startcut,startcut, ' ');
  return csSubstring;
}


void renewMessage(char *alloc)
{
  const char *command="python newsfilter.py";
  FILE *run = popen(command, "r");
  int c=0;
  int X =0;
  int n=0;
  printf("Gathering message info.\n");
  char *str = NULL;
  char buf[4096];
  size_t len = 0;
  fread(alloc, 1, 4000, run);
  alloc[4001]=0;
  printf("%s\n", alloc);
  //std::string Text(alloc);



  printf("Message of lenght %i loaded succesfully. \n", strlen(alloc));
}

int getpid(char *PID, char *procname)
{
  char output[64000];
  FILE *PS=popen("ps x", "r");

  fread(output, 1, 64000, PS);


  char *Read =strtok(output, "\n");

  while (Read!=NULL)
    {
    if ( strstr(Read, procname)!= NULL )
      {

        Read = strtok(Read, " ");
        memcpy(PID, Read, strlen(Read));
        printf("FOUND %s\n", PID);

        return 0;
      }
    else
      {
        //printf("%s\n",Read);
        Read=strtok(NULL, "\n");
      }

    }
  printf("PID not found;\n");

  return 1;
}


std::string GetStdoutFromCommand(std::string cmd)
{
  std::string data;
  FILE * stream;
  const int max_buffer = 256;
  char buffer[max_buffer];
  cmd.append(" 2>&1");

  stream = popen(cmd.c_str(), "r");
  if (stream) {
    while (!feof(stream))
      if (fgets(buffer, max_buffer, stream) != NULL) data.append(buffer);
    pclose(stream);
  }
  return data;
}
