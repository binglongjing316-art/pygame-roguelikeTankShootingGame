def count_label_sprites(groups, _label='label'):
    """
    计算精灵组中指定标签的精灵数量
    :param groups: 精灵组
    :param _label: 标签
    :return: 精灵数量
    """

    n = 0
    for _ in groups:
        if _label in _.label:
            n += 1
    return n
