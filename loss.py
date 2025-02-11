"""
Author    Daeheon Kwon (2024)
Contact   daeheonkwon00@gmail.com
Date      2024.05.04
"""

import torch

def npc_training_loss(output, model, l2_reg):
    # output: (batch_size, 16, 1)
    mean_output = torch.mean(output, dim=0)
    distances = torch.norm(mean_output.view(1, -1, 1) - model.npc.position.data, dim=1).squeeze()
    closest_position_index = torch.argmin(distances)
    closest_position = model.npc.position[closest_position_index]
    npc_loss = torch.norm(mean_output - closest_position)

    # Add L2 regularization term

    all_param = torch.cat([param.view(-1) for name, param in model.named_parameters() if 'npc.label' not in name])
    l2_loss = l2_reg * 0.5 * torch.norm(all_param) ** 2

    return npc_loss + l2_loss

def npc_validation_loss(output, model):
    # output: (batch_size, 16, 1)
    losses = []
    closest_labels = []

    for sample in output:
        distances = torch.norm(sample.view(1, -1, 1) - model.npc.position.data, dim=1).squeeze()
        closest_position_index = torch.argmin(distances)
        closest_position = model.npc.position[closest_position_index]
        loss = torch.norm(sample - closest_position)
        losses.append(loss.item())
        
        # Get the label corresponding to the closest position
        closest_label = model.npc.label[closest_position_index]
        closest_labels.append(closest_label.item())

    return loss, closest_labels
