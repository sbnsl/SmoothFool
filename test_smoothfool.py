import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
from smoothfool import smoothfool_v2
import os
from torch_utils import *


# set random seed
torch.manual_seed(263)
np.random.seed(274)


# Check for cuda devices
device = 'cuda' if torch.cuda.is_available() else 'cpu'

# net = models.densenet121(pretrained=True)
net = models.resnet101(pretrained=True)
# net = models.densenet161(pretrained=True)
# net = models.vgg19_bn(pretrained=True)
# net = models.vgg16_bn(pretrained=True)
# net = models.vgg16(pretrained=True)
# net = models.resnet152(pretrained=True)
# net = models.inception_v3(pretrained=True)


# Switch to evaluation mode
net.eval()

# read the input image
im_orig = Image.open('/home/lab320/Downloads/499510904_25d51a5a4f.jpg')
# im_orig = Image.open('/media/lab320/0274E2F866ED37FC/testextract/1/n00015388_60736.JPEG')#lion




mean = [0.485, 0.456, 0.406]
std = [0.229, 0.224, 0.225]
transforms.Compose([transforms.ToTensor(), transforms.Normalize(mean=mean, std=std)])(im_orig)

# Remove the mean

im = transforms.Compose([
    transforms.Scale(256),
    transforms.CenterCrop(224),
    transforms.ToTensor(), transforms.Normalize(mean=mean, std=std)])(im_orig)


x_adv, pred_lbl, adv_lbl = smoothfool_v2(net, im, n_clusters=8, plot_cluters=False, device=device)




labels = open(os.path.join('synset_words.txt'), 'r').read().split('\n')
str_label_orig = labels[np.int(pred_lbl)].split(',')[0]
str_label_pert = labels[np.int(adv_lbl)].split(',')[0]
print (str_label_orig)
print (str_label_pert)


print (x_adv.min(), x_adv.max())

im_np = inv_tf(im.cpu().numpy().squeeze(), mean, std)
im_adv_np = inv_tf(x_adv.cpu().numpy().squeeze(), mean, std)





print (im_np.min(), im_np.max())
print (im_adv_np.min(), im_adv_np.max())


plt.subplot(131)
plt.imshow(im_np)
plt.subplot(132)
plt.imshow(im_adv_np)
diff = torch2img(x_adv.cpu() - im.cpu())
diff = normalize(im_np-im_adv_np)
plt.subplot(133)
plt.imshow(diff)

plt.show()
