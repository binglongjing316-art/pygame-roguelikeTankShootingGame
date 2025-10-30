import pygame

from include import constant
from include.sprites_init import booms
from spirit.boom import Boom

prop_image = None


def prop_function(prop_name, user):
    if prop_name == "boom":
        for boom in booms:
            boom.explode()
        if not user.is_prop_cooling:
            boom = Boom(user.rect.centerx, user.rect.centery)
            boom.speed = user.speed
            boom.damage = user.damage * 2
            booms.add(boom)
            user.prop_cooling_count = 0
            user.is_prop_cooling = True




def prop_show(prop_name):
    global prop_image

    image_width = 0
    image_height = 0
    if prop_name == "boom":
        prop_image = pygame.image.load("image/prop/boom_prop.png")
        image_width = prop_image.get_width()
        image_height = prop_image.get_width()
    if prop_image is not None:
        constant.virtual_screen.blit(prop_image, (90 - image_width // 2, constant.SCREEN_HEIGHT - 60 - image_height))
