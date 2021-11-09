from pypylon import pylon


'''tl_factory = pylon.TlFactory.GetInstance()
devices = tl_factory.EnumerateDevices()
for device in devices:
    print(device.GetFriendlyName())'''

tl_factory = pylon.TlFactory.GetInstance()
camera = pylon.InstantCamera()
camera.Attach(tl_factory.CreateFirstDevice())

camera.Open()
camera.ExposureTime = 105000  # in us
camera.StartGrabbing(pylon.GrabStrategy_OneByOne)
grab = camera.RetrieveResult(100, pylon.TimeoutHandling_ThrowException)
if grab.GrabSucceeded():
    print('Grab succeded')

camera.Close()