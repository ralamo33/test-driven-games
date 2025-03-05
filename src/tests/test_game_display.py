def test_board_display(game):
    starting_display = """_ w _ w _ w _ w
w _ w _ w _ w _
_ w _ w _ w _ w
_ _ _ _ _ _ _ _
_ _ _ _ _ _ _ _
b _ b _ b _ b _
_ b _ b _ b _ b
b _ b _ b _ b _"""
    assert game._display() == starting_display 