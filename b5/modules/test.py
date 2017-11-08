from ..lib.module import BaseModule


class TestModule(BaseModule):
    def get_script(self):
        return '''
test:fun() {
    echo "fun"
}
        '''
