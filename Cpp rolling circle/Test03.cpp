#include <SFML/Graphics.hpp>

int main()
{
    // Create the window
    sf::RenderWindow window(sf::VideoMode(800, 600), "Rolling Ball");

    // Load the circle image
    sf::Texture texture;
    if (!texture.loadFromFile("circle.png"))
    {
        // Error handling if the image fails to load
        return -1;
    }

    // Set up the circle sprite
    sf::Sprite circleSprite(texture);
    circleSprite.setOrigin(circleSprite.getGlobalBounds().width / 2, circleSprite.getGlobalBounds().height / 2);
    circleSprite.setPosition(window.getSize().x / 2, window.getSize().y / 2);

    // Set the initial speed and direction of the circle
    float speed = 2.0f;
    bool movingLeft = false;
    bool movingRight = false;

    // Game loop
    while (window.isOpen())
    {
        sf::Event event;
        while (window.pollEvent(event))
        {
            if (event.type == sf::Event::Closed)
            {
                window.close();
            }
            else if (event.type == sf::Event::KeyPressed)
            {
                if (event.key.code == sf::Keyboard::Left)
                {
                    movingLeft = true;
                }
                else if (event.key.code == sf::Keyboard::Right)
                {
                    movingRight = true;
                }
            }
            else if (event.type == sf::Event::KeyReleased)
            {
                if (event.key.code == sf::Keyboard::Left)
                {
                    movingLeft = false;
                }
                else if (event.key.code == sf::Keyboard::Right)
                {
                    movingRight = false;
                }
            }
        }

        // Update the circle's position
        if (movingLeft && circleSprite.getPosition().x > 0)
        {
            circleSprite.move(-speed, 0);
        }
        else if (movingRight && circleSprite.getPosition().x < window.getSize().x)
        {
            circleSprite.move(speed, 0);
        }

        // Clear the window
        window.clear();

        // Draw the circle
        window.draw(circleSprite);

        // Display the window
        window.display();
    }

    return 0;
}