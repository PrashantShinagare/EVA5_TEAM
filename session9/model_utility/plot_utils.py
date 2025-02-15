import matplotlib.pyplot as plt
import numpy as np


# functions to show an image
def imshow(img):
    img = img / 2 + 0.5     # unnormalize
    npimg = img.numpy()
    plt.imshow(np.transpose(npimg, (1, 2, 0)))

def plot_model_history(title_name, train_acc_hist, test_acc_hist, train_loss_hist, test_loss_hist, save_filename,path ):
    fig, axs = plt.subplots(1,2,figsize=(20,5))
    # summarize history for accuracy
    x_size = len(train_acc_hist)
    legend_list = ['train', 'test']

    axs[0].plot(range(1,x_size+1), train_acc_hist)
    axs[0].plot(range(1,x_size+1), test_acc_hist)

    title = '{} - Accuracy'.format(title_name)
    axs[0].set_title(title)
    axs[0].set_ylabel('Accuracy')
    axs[0].set_xlabel('Epoch')
    axs[0].set_xticks(np.arange(1,x_size+1),x_size/10)
    axs[0].legend(legend_list, loc='best')

   # plot losses
    axs[1].plot(range(1,x_size+1),train_loss_hist)
    axs[1].plot(range(1,x_size+1),test_loss_hist)

    title = '{} - Losses'.format(title_name)
    axs[1].set_title(title)
    axs[1].set_ylabel('Loss')
    axs[1].set_xlabel('Epoch')
    axs[1].set_xticks(np.arange(1,x_size+1),x_size/10)
    axs[1].legend(legend_list, loc='best')
    plt.show()
    fig.savefig("{}.jpg".format(path + save_filename))


def plot_model_comparison(legend_list, model1_acc_hist, model1_loss_hist,
                          model2_acc_hist, model2_loss_hist,
                          model3_acc_hist, model3_loss_hist,
                          model4_acc_hist, model4_loss_hist,):
    fig, axs = plt.subplots(1,2,figsize=(20,5))
    # summarize history for accuracy
    x_size = len(model1_acc_hist)
    
    axs[0].plot(range(1,x_size+1), model1_acc_hist)
    axs[0].plot(range(1,x_size+1), model2_acc_hist)
    axs[0].plot(range(1,x_size+1), model3_acc_hist)
    axs[0].plot(range(1,x_size+1), model4_acc_hist)
    
    axs[0].set_title('Model Accuracy')
    axs[0].set_ylabel('Accuracy')
    axs[0].set_xlabel('Epoch')
    axs[0].set_xticks(np.arange(1,x_size+1),x_size/10)
    axs[0].legend(legend_list, loc='best')
    
    # plot losses
    axs[1].plot(range(1,x_size+1),model1_loss_hist)
    axs[1].plot(range(1,x_size+1),model2_loss_hist)
    axs[1].plot(range(1,x_size+1),model3_loss_hist)
    axs[1].plot(range(1,x_size+1),model4_loss_hist)
    axs[1].set_title('Model Losses')
    axs[1].set_ylabel('Loss')
    axs[1].set_xlabel('Epoch')
    axs[1].set_xticks(np.arange(1,x_size+1),x_size/10)
    axs[1].legend(legend_list, loc='best')
    plt.show()
    fig.savefig('/home/jd/Desktop/EVA5/session9/image/'+'model_compare.jpg')


def miss_classification(model, device, classes, testloader,path,typ_of_file, num_of_images = 20, save_filename="misclassified"):
    model.eval()
    misclassified_cnt = 0
    fig = plt.figure(figsize=(10,9))
    for data, target in testloader:
        data, target = data.to(device), target.to(device)
        output = model(data)
        pred = output.argmax(dim=1, keepdim=True)     # get the index of the max log-probability
        pred_marker = pred.eq(target.view_as(pred))   
        wrong_idx = (pred_marker == False).nonzero()  # get indices for wrong predictions
        for idx in wrong_idx:
            index = idx[0].item()
            title = "T:{}, P:{}".format(classes[target[index].item()], classes[pred[index][0].item()])
            #print(title)
            ax = fig.add_subplot(4, 5, misclassified_cnt+1, xticks=[], yticks=[])
            #ax.axis('off')
            ax.set_title(title)
            #plt.imshow(data[index].cpu().numpy().squeeze(), cmap='gray_r')
            imshow(data[index].cpu())

            misclassified_cnt += 1
            if(misclassified_cnt==num_of_images):
                break

        if(misclassified_cnt==num_of_images):
            break

    fig.savefig( path +typ_of_file + '_missclassified_images'+ '.jpg')
    return


def plot_dataset_images(device, classes, data_loader, save_path,num_of_images=20,):
    cnt = 0
    fig = plt.figure(figsize=(10,9))
    for data, target in data_loader:
        data, target = data.to(device), target.to(device)
        for index, label in enumerate(target):
            title = "{}".format(classes[label.item()])
            
            ax = fig.add_subplot(4, 5, cnt+1, xticks=[], yticks=[])
            ax.set_title(title)
            imshow(data[index].cpu())
        
            cnt += 1
            if(cnt==num_of_images):
                break
        if(cnt==num_of_images):
            break
    fig.savefig(save_path +'random_image'+'.jpg')
    return