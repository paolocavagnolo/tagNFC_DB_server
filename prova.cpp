// Example program
#include <iostream>
#include <string>

float bytes2float(unsigned char a, unsigned char b, unsigned char c, unsigned char d);

int main()
{

  std::cout << "Hello, " << bytes2float('\x00','\x00','\xc7','B') << "!\n";
}

float bytes2float(unsigned char a, unsigned char b, unsigned char c, unsigned char d) {
  float snelheid;

  union u_tag {
    unsigned char b[4];
    float fval;
  } u;

  u.b[0] = a;
  u.b[1] = b;
  u.b[2] = c;
  u.b[3] = d;

  return snelheid = u.fval;
}
