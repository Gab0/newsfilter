#ifndef SCROLLER_H
#define SCROLLER_H

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

#endif
