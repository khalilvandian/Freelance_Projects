#include <iostream>
#include <SDL.h>

using namespace std;

// Set Window size and ball image size
const float WINDOW_WIDTH = 800;
const float WINDOW_HEIGHT = 600;
const float BALL_SIZE = 64;

int main(int argc, char* argv[])
{
    //Initiate SDL and define window and renderer for the program
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window* window = SDL_CreateWindow("Ball",
        SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
        WINDOW_WIDTH, WINDOW_HEIGHT, SDL_WINDOW_SHOWN);
    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1,
        SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);

    // Load the image of the ball into the program
    SDL_Surface* ballSurface = SDL_LoadBMP("image.bmp");
    SDL_Texture* ballTexture = SDL_CreateTextureFromSurface(renderer, ballSurface);
    SDL_FreeSurface(ballSurface);

    // assign float amounts of ball's initial position into ballRect Struct. Ball will appear in the center of the window.
    SDL_FRect ballRect;
    ballRect.x = (WINDOW_WIDTH - BALL_SIZE) / 2;
    ballRect.y = (WINDOW_HEIGHT - BALL_SIZE) / 2;
    ballRect.w = BALL_SIZE;
    ballRect.h = BALL_SIZE;

    // Flags for keeping record of the ball's status
    // moving = is ball moving
    // rotating = is ball rotating
    // upArrowPressed = is the up arrow key on the keboard kept pressed.
    // downArrowPressed = is the down arrow key on the keboard kept pressed.
    bool moving = false;
    bool rotating = false;
    bool upArrowPressed = false;
    bool downArrowPressed = false;

    // Variables for holding the values for ball's speed, angle and movement direction are defined.
    float rotationAngle = 0;
    float direction = 0;
    float ball_speed = 1;

    // Variables for holding the previous mouse cursor position are defined. this will be used in detecting clockwise and counterclockwise movement of the cursor.
    int prevX = 0;
    int prevY = 0;

    SDL_Event event;
    bool running = true;

    while (running)
    {
        while (SDL_PollEvent(&event))
        {
            // If an event is raised, act according to the cases.
            switch (event.type)
            {
            case SDL_QUIT:
                running = false;
                break;

            // if a key is down
            case SDL_KEYDOWN:
                switch (event.key.keysym.sym)
                {
                // If the key is the right arrow, the ball will move and rotate rightwards.
                case SDLK_RIGHT:
                    moving = true;
                    rotating = true;
                    direction = 1;
                    if (ball_speed < 0.5)
                    {
                        ball_speed = 1;
                    }

                    break;

                // If the key is the left arrow, the ball will move and rotate leftwards.
                case SDLK_LEFT:
                    moving = true;
                    rotating = true;
                    direction = -1;
                    if (ball_speed < 0.5)
                    {
                        ball_speed = 1;
                    }
                    break;

                // If the key is the up arrow, the ball will speed up.
                case SDLK_UP:
                    // make sure speed is only increased one level for each time the up key is pressed.
                    if (!upArrowPressed)
                    {
                        upArrowPressed = true;
                        ball_speed += 0.1;
                    }
                    break;

                // If the key is the down arrow, the ball will speed down.
                case SDLK_DOWN:
                    // make sure speed is only increased one level for each time the down key is pressed.
                    if (!downArrowPressed)
                    {
                        downArrowPressed = true;
                        if (ball_speed - 0.1 >= 0)
                        {
                            ball_speed -= 0.1;
                        }
                        else
                        {
                            ball_speed = 0;
                        }
                    }
                    break;

                }
                break;

            // if a key is released.
            case SDL_KEYUP:
                switch (event.key.keysym.sym)
                {
                // if it's the up key, change the flag.
                case SDLK_UP:
                    upArrowPressed = false;
                    break;

                // if it's the down key, change the flag.
                case SDLK_DOWN:
                    downArrowPressed = false;
                    break;
                }
                break;

            case SDL_MOUSEMOTION:
                // Get current position of the mouse
                int x = event.motion.x - WINDOW_WIDTH / 2;
                int y = -event.motion.y + WINDOW_HEIGHT / 2;
                // Check for clockwise movement
                int deltaX = x - prevX;
                int deltaY = y - prevY;

                //For every quarter of the cartesian coordinates an specific condition is set to detect 
                //clockwise and counter clockwise movement. for instance if the cursor is in the first 
                //quarter, it must have a negative movement slope to be considered a clockwise movement.
                bool clockwise1 = (deltaX > 0) && (deltaY < 0) && (x > 0) && (y > 0);
                bool clockwise2 = (deltaX > 0) && (deltaY > 0) && (x < 0) && (y > 0);
                bool clockwise3 = (deltaX < 0) && (deltaY > 0) && (x < 0) && (y < 0);
                bool clockwise4 = (deltaX < 0) && (deltaY < 0) && (x > 0) && (y < 0);

                bool counterClockwise1 = (deltaX < 0) && (deltaY > 0) && (x > 0) && (y > 0);
                bool counterClockwise2 = (deltaX < 0) && (deltaY < 0) && (x < 0) && (y > 0);
                bool counterClockwise3 = (deltaX > 0) && (deltaY < 0) && (x < 0) && (y < 0);
                bool counterClockwise4 = (deltaX > 0) && (deltaY > 0) && (x > 0) && (y < 0);

                if (clockwise1 || clockwise2 || clockwise3 || clockwise4) {
                    // Clockwise movement detected
                    ball_speed += 0.1;

                }
                else if (counterClockwise1 || counterClockwise2 || counterClockwise3 || counterClockwise4)
                {
                    // Counter Clockwise movement detected
                    if (ball_speed - 0.1 >= 0)
                    {
                        ball_speed -= 0.1;
                    }
                    else
                    {
                        ball_speed = 0;
                    }

                }
                // Update previous position
                prevX = x;
                prevY = y;
                break;
            }
        }

        // If the ball is in a moving status change it's direction in accordance with ball speed and the direction
        if (moving)
        {
            ballRect.x += direction * ball_speed;

            // If the ball reaches the boarder, make it stop rolling.
            if (ballRect.x >= WINDOW_WIDTH - BALL_SIZE)
            {
                ballRect.x = WINDOW_WIDTH - BALL_SIZE;
                moving = false;
                rotating = false;
            }
            else if (ballRect.x <= 0)
            {
                ballRect.x = 0;
                moving = false;
                rotating = false;
            }
        }

        // If the ball is in a rotaing status change its angle in accordance with direction and ball speed.
        if (rotating)
        {
            rotationAngle += direction * ball_speed;
            if (rotationAngle >= 360)
            {
                rotationAngle -= 360;
            }
            else if (rotationAngle <= 0)
            {
                rotating += 360;
            }
        }

        // render the graphic according to the ball status
        SDL_RenderClear(renderer);
        SDL_RenderCopyExF(renderer, ballTexture, NULL, &ballRect, rotationAngle, NULL, SDL_FLIP_NONE);
        SDL_RenderPresent(renderer);
    }

    // If the program is cloased, close sdl entities.
    SDL_DestroyTexture(ballTexture);
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;
}
