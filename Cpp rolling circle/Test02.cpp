#include <iostream>
#include <conio.h>
#include <windows.h>

const int WINDOW_WIDTH = 80;
const int SPEED = 5;

void clearScreen() {
    COORD cursorPosition;
    cursorPosition.X = 0;
    cursorPosition.Y = 0;
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), cursorPosition);
}

void drawCircle(int x, int y) {
    std::cout << "O";
    COORD cursorPosition;
    cursorPosition.X = x;
    cursorPosition.Y = y;
    SetConsoleCursorPosition(GetStdHandle(STD_OUTPUT_HANDLE), cursorPosition);
}

void moveCircle(int& x, int direction) {
    if (direction == -1 && x > 0) {
        drawCircle(x--, 0);
        Sleep(SPEED);
    }
    else if (direction == 1 && x < WINDOW_WIDTH) {
        drawCircle(x++, 0);
        Sleep(SPEED);
    }
}

int main() {
    int x = WINDOW_WIDTH / 2;  // Starting position of the circle
    int direction = 0;  // -1 for left, 1 for right

    // Hide the console cursor
    HANDLE consoleHandle = GetStdHandle(STD_OUTPUT_HANDLE);
    CONSOLE_CURSOR_INFO cursorInfo;
    cursorInfo.dwSize = 100;
    cursorInfo.bVisible = FALSE;
    SetConsoleCursorInfo(consoleHandle, &cursorInfo);

    while (true) {
        if (_kbhit()) {
            char key = _getch();
            if (key == 27) {  // ESC key
                break;
            }
            else if (key == 75) {  // Left arrow key
                direction = -1;
            }
            else if (key == 77) {  // Right arrow key
                direction = 1;
            }
        }
        moveCircle(x, direction);
    }

    // Show the console cursor again
    cursorInfo.bVisible = TRUE;
    SetConsoleCursorInfo(consoleHandle, &cursorInfo);

    return 0;
}