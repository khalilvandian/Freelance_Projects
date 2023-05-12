#include <iostream>
#include <SDL.h>

const int WINDOW_WIDTH = 1600;
const int WINDOW_HEIGHT = 1200;

const int BALL_SIZE = 64;
const int BALL_SPEED = 5;

int main(int argc, char* argv[])
{
    SDL_Init(SDL_INIT_VIDEO);

    SDL_Window* window = SDL_CreateWindow("Ball",
        SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED,
        WINDOW_WIDTH, WINDOW_HEIGHT, SDL_WINDOW_SHOWN);
    SDL_Renderer* renderer = SDL_CreateRenderer(window, -1,
        SDL_RENDERER_ACCELERATED | SDL_RENDERER_PRESENTVSYNC);

    SDL_Surface* ballSurface = SDL_LoadBMP("image.bmp");
    SDL_Texture* ballTexture = SDL_CreateTextureFromSurface(renderer, ballSurface);
    SDL_FreeSurface(ballSurface);

    SDL_Rect ballRect;
    ballRect.x = (WINDOW_WIDTH - BALL_SIZE) / 2;
    ballRect.y = (WINDOW_HEIGHT - BALL_SIZE) / 2;
    ballRect.w = BALL_SIZE;
    ballRect.h = BALL_SIZE;

    bool moving = false;
    bool rotating = false;

    int rotationAngle = 0;

    SDL_Event event;
    bool running = true;
    while (running)
    {
        while (SDL_PollEvent(&event))
        {
            switch (event.type)
            {
            case SDL_QUIT:
                running = false;
                break;
            case SDL_KEYDOWN:
                switch (event.key.keysym.sym)
                {
                case SDLK_RIGHT:
                    moving = true;
                    rotating = true;
                    break;
                }
                break;
            case SDL_KEYUP:
                switch (event.key.keysym.sym)
                {
                case SDLK_RIGHT:
                    moving = false;
                    rotating = false;
                    break;
                }
                break;
            }
        }

        if (moving)
        {
            ballRect.x += BALL_SPEED;
            if (ballRect.x >= WINDOW_WIDTH - BALL_SIZE)
            {
                ballRect.x = WINDOW_WIDTH - BALL_SIZE;
                moving = false;
                rotating = false;
            }
        }

        if (rotating)
        {
            rotationAngle += BALL_SPEED;
            if (rotationAngle >= 360)
            {
                rotationAngle -= 360;
            }
        }

        SDL_RenderClear(renderer);
        SDL_RenderCopyEx(renderer, ballTexture, NULL, &ballRect, rotationAngle, NULL, SDL_FLIP_NONE);
        SDL_RenderPresent(renderer);
    }

    SDL_DestroyTexture(ballTexture);
    SDL_DestroyRenderer(renderer);
    SDL_DestroyWindow(window);
    SDL_Quit();

    return 0;
}
