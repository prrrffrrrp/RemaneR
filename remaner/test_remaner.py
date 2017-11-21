from .renamer import InputCheckExtract, Renamer, extension, natural_key


def test_extension():
    assert extension('lorem.odt') == '.odt'
    assert extension('lorem.odt', 'ipsum') == '.odt'
    assert extension('-*-') == ''
    assert extension('lorem.odt', '-*-') == ''
    assert extension('lorem') == ''
    assert extension('lorem', 'ipsum') == ''
