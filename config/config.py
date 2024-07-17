URL = 'https://my.sifly.global/en/login'
USERNAME_FIELD = 'mat-input-0'
PASSWORD_FIELD = 'mat-input-1'
LOGIN_BUTTON = '/html/body/app-root/div/div/app-login/div/form/div[1]/button'
DEVICES_TAB = '/html/body/app-root/div/mat-toolbar/div/a[2]'
SELECT_DEVICE_TYPE = 'mat-select-0'
SELECT_TYPE = 'mat-option-12' # hydrofoil option in the dropdown menu 
INPUT_SERIAL_NUMBER = 'mat-input-4'
FIRST_DEVICE = '/html/body/app-root/div/div/app-device-list/form/div[3]/table/tbody/tr/td[1]/button/span/span'
EDIT_DEVICE_VERSION = "//*[contains(@class, 'fa-pen')]"
SELECT_SPECIFIC_VERSION = "/html/body/div[2]/div[2]/div/mat-dialog-container/app-device-specific-sw-edit/form/mat-radio-group/mat-radio-button[2]/label/div[2]"
SELECT_DEVICE_VERSION = "/html/body/div[2]/div[2]/div/mat-dialog-container/app-device-specific-sw-edit/form/mat-form-field/div/div[1]/div/mat-select/div/div[1]/span/span"
SELECT_LAST_VERSION = "/html/body/div[2]/div[4]/div/div/div/mat-option[2]/span"
STATE ="/html/body/app-root/div/div/app-device-details/form/div/div[2]/div[3]/div/div[2]/div[2]/div"
SAVE_VERSION_BUTTON = "/html/body/div[2]/div[2]/div/mat-dialog-container/app-device-specific-sw-edit/form/div[2]/button[1]"
DERIGISTERATE_BTN = "//span[@class='mat-button-wrapper' and contains(text(), 'Deregistration')]"
DERIGISTERATE_CONFIRM_BTN = "/html/body/div[2]/div[2]/div/mat-dialog-container/app-device-dereg/form/div[3]/button[1]/span"
REGISTERATE_DEVICE_BTN = "//span[@class='mat-button-wrapper' and contains(text(), 'Registration')]"
SELECT_REGISTRATOR = "//*[contains(@class, 'fa-search')]"
SELECT_FIRST_REGISTRATOR = "(//*[contains(@class, 'fa-square')])[1]"
REGISTERATE_CONFIRM_BTN = "/html/body/div[2]/div[2]/div/mat-dialog-container/app-device-reg/form/div[3]/button[1]"

# Current test
# //////////////////////////////////////////////
CURRENT_USERNAME = 'abachev'
CURRENT_PASSWORD = 'RideTheWaves@8am'
CURRENT_SERIAL_NUM  = '53998'