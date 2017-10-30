#include <stdio.h>
#include <cstdlib>
#include <string.h>
#include <unistd.h>
#include <locale.h>

#include <iostream>
#include <locale>
#include <fstream>
#include <string>
#include <algorithm>
#include <future>
#include <sstream>
#include <vector>
#include <iterator>

#define bad(x) (aStr[x] < 0)

std::string GetStdoutFromCommand(std::string cmd);

std::string utf8substr(std::string originalString, int SubStrStart, int SubStrLength);

std::string getHyperlink(std::vector<std::string> hyperlinks, int index);

FILE *getStdinAddress(std::string targetname);
std::vector<std::string> split(const std::string &s, char delim);

template<typename Out> void Split(const std::string &s, char delim, Out result);

template<typename Out>
void Split(const std::string &s, char delim, Out result)
{
  std::stringstream ss(s);
  std::string item;
  while (std::getline(ss, item, delim))
    {
    *(result++) = item;
  }
}

std::vector<std::string> split(const std::string &s, char delim)
{
  std::vector<std::string> elems;
  Split(s, delim, std::back_inserter(elems));
  return elems;
}

FILE *getStdinAddress(std::string targetname)
{

    char output[64000];
    FILE *PS=popen("ps x", "r");

    fread(output, 1, 64000, PS);

    char *Read =strtok(output, "\n");
    char *PID= NULL;
    while (Read!=NULL)
      {
        if ( strstr(Read, targetname.c_str())!= NULL )
          {

            Read = strtok(Read, " ");
            memcpy(PID, Read, strlen(Read));
            //printf("FOUND %s\n", PID);

            return 0;
          }
        else
          {
            //printf("%s\n",Read);
            Read=strtok(NULL, "\n");
          }

      }
    //printf("PID not found;\n");
    std::string path("/proc/");
    path += PID;
    path += "/fd/0";

    FILE *targetstdin = fopen(path.c_str(), "a");
    return targetstdin;

}

int main(int argc, char **argv)
{

  int STEP= 1;
  float SLEEPTIME = 0.5;

  char *StatusBarPID = (char *)malloc(100 * sizeof(char));

  char *outpath = (char *)malloc(100 * sizeof(char));
  //printf("Writing to %s.\n", outpath);
  if (argc == 1)
    {
      std::cout << "Message appendage script not specified;; abort.\n";
      exit(1);
    }

  //printf("Getting PID of %s\n", outputprocname);

  //if (getpid(StatusBarPID, outputprocname))
  //  return 1;

  //printf("Endpoint PID %s\n", StatusBarPID);
  //asprintf(&outpath, "/proc/%s/fd/0", StatusBarPID);

  //FILE *output = fopen( outpath, "a" );

  int commresult =0;
  int horizontalspan = 116;
  //printf("Writing to %s\n\n", outpath);
  int waitingData=0;

  std::string Text;
  std::string OutputText;
  std::string IncomingData;
  std::future<std::string> ID;
  int Division=0;
  for (;;)
    {
      //printf("text length = %i\n", Text.length());
      if (Text.length() < horizontalspan)
        {
          if (!waitingData)
            {
              ID = std::async(GetStdoutFromCommand, argv[1]);
              waitingData++;

            }
          if (waitingData > 8)
            {
              printf("iiih\n");
              ID.wait();
              IncomingData = ID.get();
              std::cout << IncomingData;
              Division = IncomingData.find("###");
              std::cout << Division;

              Text.insert(Text.length(), IncomingData.substr(2, Division), 0, std::string::npos);

              std::vector<std::string> hyperlinks = split(IncomingData.substr(Division, -1), '=');
              waitingData=0;
            }
          else if (waitingData)
            waitingData++;
        }
      if (Text.length())

        {
      Text = Text.substr(STEP, Text.length());
      OutputText = utf8substr(Text, 1, horizontalspan);
      OutputText += "\n";


      //std::fprintf(output, "%s", OutputText.c_str());
      std::cout << OutputText;

      if (commresult<0)
        return 1;
      fflush(stdout);

      //printf("Success %i\n\n", commresult);
        }
      usleep((int)(SLEEPTIME * 1000000));

    }
  return 0;
}

std::string getHyperlink(std::vector<std::string> hyperlinks, int index)
{
  std::string matchlink;
  for (int W;W<hyperlinks.size();W++)
    {
      std::vector<std::string> Link = split(hyperlinks[W], ';');
      if (std::stoi(Link[0]) > index)
        {
          return matchlink;

        }
      matchlink = Link[1];

    }

  return matchlink;

}
std::string utf8substr(std::string originalString, int SubStrStart, int SubStrLength)
{
  int len = 0, byteIndex = 0;
  const char* aStr = originalString.c_str();
  size_t origSize = originalString.size();

  int SubStrEnd = SubStrStart + SubStrLength-1;
  int endcut=0, startcut=0;


  // START-POINT-TRIM;
  /*
  printf( "Before Start %i\n", aStr[SubStrStart-1]  );
  printf( "On Start %i\n", aStr[SubStrStart] );
  printf( "After Start %i\n", aStr[SubStrStart+1] );
  printf( "Two After Start %i\n\n", aStr[SubStrStart+2 ]);
  */
  if bad(SubStrStart-1)
          {
            while bad(SubStrStart+startcut)
                       startcut+=1;
          }

  // END-POINT-TRIM;
  /*
  printf( "Before End %i\n", aStr[SubStrEnd-1]  );
  printf( "On End  %i\n", aStr[SubStrEnd]);
  printf( "After End %i\n", aStr[SubStrEnd+1]);
  */
  if bad(SubStrEnd+1)
          {
            while bad(SubStrEnd-endcut)
                       endcut--;

            SubStrLength-=endcut;
          }
  //printf("%i;%i\n", startcut,endcut);
  std:: string csSubstring= originalString.substr(SubStrStart, SubStrLength);
  csSubstring.replace(0,startcut,startcut, ' ');
  return csSubstring;
}


std::string GetStdoutFromCommand(std::string cmd)
{
  std::string data;
  FILE * stream;
  const int max_buffer = 256;
  char buffer[max_buffer];
  cmd.append(" 2>&1");

  stream = popen(cmd.c_str(), "r");
  if (stream)
    {
      while (!feof(stream))
        if (fgets(buffer, max_buffer, stream) != NULL) data.append(buffer);
      pclose(stream);
    }
  data.erase(std::remove(data.begin(), data.end(), '\n'), data.end());
  return data;
}
