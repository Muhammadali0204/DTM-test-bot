from aiogram.fsm.state import StatesGroup, State



class SignUp(StatesGroup):
    ism_yuborish = State()


class TestIshlash(StatesGroup):
    test_turi = State()
    

class Sozlamalar(StatesGroup):
    sozlamalar = State()
    get_new_name = State()


class AdminStates(StatesGroup):
    get_file = State()
    
class SendMessageStates(StatesGroup):
    get_sending_message = State()
    get_btn_name_sending_msg = State()
    get_btn_url_sending_msg = State()
