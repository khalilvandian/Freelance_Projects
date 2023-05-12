#include <SDL.h>
#include <SDL_image.h>
#include <cmath>

const int WINDOW_WIDTH = 1280;
const int WINDOW_HEIGHT = 720;
const int BALL_SIZE = 64;
const int BALL_SPEED = 1;

int main(int argc, char* argv[])
{
    // Initialize SDL
    SDL_Init(SDL_INIT_VIDEO);

    // Initialize SDL_image library
    IMG_Init(IMG_INIT_PNG);

    // Create a window
    SDL_Window* window = SDL_CreateWindow("Moving Ball", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, WINDOW_WIDTH, WINDOW_HEIGHT, SDL_WINDOW_SHOWN);

    // Create a renderer
    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_ACCELERATED);

    // Load the image
    SDL_Surface* imageSurface = IMG_Load("ball.png");
    SDL_Texture* ballTexture = SDL_CreateTextureFromSurface(renderer, imageSurface);

    // Set the initial position of the ball
    SDL_Rect ballRect = { 0, WINDOW_HEIGHT / 2 - BALL_SIZE / 2, BALL_SIZE, BALL_SIZE };

    // Set the initial direction of the ball
    int direction = 1;

    // Main loop
    bool quit = false;
    while (!quit)
    {
        // Handle events
        SDL_Event event;
        while (SDL_PollEvent(&event))
        {
            if (event.type == SDL_QUIT)
            {
                quit = true;
            }
        }

        // Move the ball
        ballRect.x += direction * BALL_SPEED;

        // Check if the ball hits the borders
        if (ballRect.x < 0 || ballRect.x > WINDOW_WIDTH - BALL_SIZE)
        {
            direction = -direction;
        }

        // Calculate the rotation angle based on the ball's direction
        double angle = direction > 0 ? 0 : M_PI;

        // Clear the screen
        SDL_SetRenderDrawColor(renderer, 0, 0, 0, 255);
        SDL_RenderClear(renderer);

        // Render the ball texture with rotation
        SDL_RenderCopyEx(renderer, ballTexture, NULL, &ballRect, angle, NULL, SDL_FLIP_NONE);

        // Update the screen
        SDL_RenderPresent(renderer);
    }

    // Clean up
    SDL_DestroyTexture(ballTexture);
    SDL_FreeSurface(imageSurface);
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    IMG_Quit();
    SDL_Quit();

    return 0;
}
