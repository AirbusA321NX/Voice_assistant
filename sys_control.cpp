// sys_control.cpp
#include <iostream>
#include <string>

using namespace std;

int main(int argc, char* argv[]) {
    if (argc < 2) {
        cout << "No command provided" << endl;
        return 1;
    }

    // Combine all arguments into one command string
    string command;
    for (int i = 1; i < argc; i++) {
        if (i > 1) command += " ";
        command += argv[i];
    }

    cout << "Executing: " << command << endl;

    int result = system(command.c_str());

    if (result != 0) {
        cerr << "Command failed with exit code " << result << endl;
    }

    return 0;
}
