import turtle
import math

class SpaceInvaders:
    def __init__(self):
        self.screen = turtle.Screen()
        self.screen.title("Space Invaders")
        self.screen.bgcolor("black")
        self.screen.setup(width=800, height=600)
        self.screen.tracer(0)

        self.player = Player()
        self.enemies = []
        for i in range(20):
            enemy = Enemy(i)
            self.enemies.append(enemy)

        self.score = 0
        self.score_marker = ScoreMarker()
        self.lives = 3
        self.lives_marker = LivesMarker()

        self.screen.listen()
        self.screen.onkey(self.player.move_left, "Left")
        self.screen.onkey(self.player.move_right, "Right")
        self.screen.onkey(self.player.shoot, "space")

        self.enemy_dx = 0.1
        self.enemy_dy = -5

    def run(self):
        while True:
            self.screen.update()

            for enemy in self.enemies:
                enemy.move(self.enemy_dx)

                if self.player.bullet and enemy.is_collision(self.player.bullet):
                    self.player.clear_bullet()
                    enemy.destroy()
                    self.enemies.remove(enemy)
                    self.score += 10
                    self.score_marker.update_score(self.score)

            if self.enemies:
                leftmost_enemy_x = min(enemy.xcor() for enemy in self.enemies)
                rightmost_enemy_x = max(enemy.xcor() for enemy in self.enemies)
                if rightmost_enemy_x > 385 or leftmost_enemy_x < -385:
                    self.enemy_dx *= -1
                    for enemy in self.enemies:
                        enemy.move_down(self.enemy_dy)

            if self.player.bullet:
                self.player.bullet.move()
                if self.player.bullet.ycor() > 300:
                    self.player.clear_bullet()

            if not self.enemies:
                self.score_marker.show_congratulations()
                break

        self.screen.mainloop()

class Player(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.shape("triangle")
        self.color("blue")
        self.penup()
        self.speed(0)
        self.goto(0, -250)
        self.setheading(90)
        self.bullet = None

    def move_left(self):
        x = self.xcor()
        x -= 4
        if x < -385:
            x = -385
        self.setx(x)

    def move_right(self):
        x = self.xcor()
        x += 4
        if x > 385:
            x = 385
        self.setx(x)

    def shoot(self):
        if not self.bullet:
            x = self.xcor()
            y = self.ycor() + 10
            self.bullet = Bullet(x, y)

    def clear_bullet(self):
        self.bullet.clear()
        self.bullet.hideturtle()
        self.bullet = None

class Enemy(turtle.Turtle):
    def __init__(self, index):
        super().__init__()
        self.shape("triangle")
        self.color("red")
        self.penup()
        self.speed(0)
        self.setheading(270)
        self.index = index
        x = -190 + (self.index % 10) * 40
        y = 250 - (self.index // 10) * 40
        self.goto(x, y)

    def move(self, dx):
        x = self.xcor()
        x += dx
        self.setx(x)

    def move_down(self, dy):
        y = self.ycor()
        y += dy
        self.sety(y)

    def destroy(self):
        self.clear()
        self.hideturtle()

    def is_collision(self, other):
        distance = math.sqrt(math.pow(self.xcor() - other.xcor(), 2) + math.pow(self.ycor() - other.ycor(), 2))
        return distance < 15

class Bullet(turtle.Turtle):
    def __init__(self, x, y):
        super().__init__()
        self.shape("square")
        self.color("white")
        self.penup()
        self.speed(0)
        self.goto(x, y)
        self.setheading(90)
        self.shapesize(stretch_wid=0.3, stretch_len=0.1)

    def move(self):
        y = self.ycor()
        y += 2
        self.sety(y)

class ScoreMarker(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.speed(0)
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(-380, 260)
        self.write("Score: 0", align="left", font=("Courier", 16, "normal"))

    def update_score(self, score):
        self.clear()
        self.write(f"Score: {score}", align="left", font=("Courier", 16, "normal"))

    def show_congratulations(self):
        self.clear()
        self.goto(0, 0)
        self.write("Congratulations!\nYou destroyed all enemies!", align="center", font=("Courier", 24, "normal"))

class LivesMarker(turtle.Turtle):
    def __init__(self):
        super().__init__()
        self.speed(0)
        self.color("white")
        self.penup()
        self.hideturtle()
        self.goto(300, 260)
        self.write("Lives: 3", align="right", font=("Courier", 16, "normal"))

space_invaders = SpaceInvaders()
space_invaders.run()

