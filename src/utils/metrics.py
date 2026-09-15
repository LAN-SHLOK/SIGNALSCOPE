import numpy as np
from sklearn.metrics import roc_auc_score, f1_score, accuracy_score, confusion_matrix, roc_curve
import matplotlib.pyplot as plt
from typing import Dict, List, Any

def compute_all_metrics(
    y_true: np.ndarray, 
    y_probs: np.ndarray, 
    attr_true: np.ndarray = None, 
    attr_preds: np.ndarray = None, 
    threshold: float = 0.5
) -> Dict[str, Any]:
    """
    Computes standard evaluation metrics for binary and optional attribution classification.
    """
    y_true = np.asarray(y_true, dtype=int)
    y_probs = np.asarray(y_probs, dtype=float)
    y_pred = (y_probs >= threshold).astype(int)
    
    auc = float(roc_auc_score(y_true, y_probs)) if len(np.unique(y_true)) > 1 else 0.0
    f1 = float(f1_score(y_true, y_pred, zero_division=0))
    acc = float(accuracy_score(y_true, y_pred))
    cm = confusion_matrix(y_true, y_pred)
    
    if cm.shape == (2, 2):
        tn, fp, fn, tp = cm.ravel()
        tpr = float(tp / (tp + fn)) if (tp + fn) > 0 else 0.0
        fpr = float(fp / (fp + tn)) if (fp + tn) > 0 else 0.0
    else:
        tpr = 0.0
        fpr = 0.0
        
    res = {
        'AUC': auc,
        'binary_auc': auc,
        'F1': f1,
        'binary_f1': f1,
        'accuracy': acc,
        'FPR': fpr,
        'TPR': tpr,
        'confusion_matrix': cm
    }
    
    if attr_true is not None and attr_preds is not None and len(attr_true) > 0:
        attr_true = np.asarray(attr_true)
        attr_preds = np.asarray(attr_preds)
        attr_acc = float(accuracy_score(attr_true, attr_preds))
        res['attr_accuracy'] = attr_acc
    else:
        res['attr_accuracy'] = 0.0
        
    return res

def compute_ece(y_true: np.ndarray, y_probs: np.ndarray, n_bins: int = 15) -> float:
    """
    Computes Expected Calibration Error.
    """
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    bin_lowers = bin_boundaries[:-1]
    bin_uppers = bin_boundaries[1:]
    
    ece = 0.0
    for bin_lower, bin_upper in zip(bin_lowers, bin_uppers):
        in_bin = (y_probs > bin_lower) & (y_probs <= bin_upper)
        prop_in_bin = in_bin.mean()
        if prop_in_bin > 0:
            accuracy_in_bin = y_true[in_bin].mean()
            avg_confidence_in_bin = y_probs[in_bin].mean()
            ece += np.abs(avg_confidence_in_bin - accuracy_in_bin) * prop_in_bin
            
    return ece

def plot_confusion_matrix(y_true: np.ndarray, y_pred: np.ndarray, classes: List[str], save_path: str):
    """
    Saves a plot of the confusion matrix.
    """
    cm = confusion_matrix(y_true, y_pred)
    fig, ax = plt.subplots()
    cax = ax.matshow(cm, cmap=plt.cm.Blues)
    plt.title('Confusion Matrix')
    fig.colorbar(cax)
    
    ax.set_xticks(np.arange(len(classes)))
    ax.set_yticks(np.arange(len(classes)))
    ax.set_xticklabels(classes, rotation=45)
    ax.set_yticklabels(classes)
    
    plt.xlabel('Predicted')
    plt.ylabel('True')
    
    for i in range(cm.shape[0]):
        for j in range(cm.shape[1]):
            ax.text(j, i, str(cm[i, j]), va='center', ha='center')
            
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def plot_roc_curve(y_true: np.ndarray, y_probs: np.ndarray, save_path: str):
    """
    Saves a plot of the ROC curve.
    """
    if len(np.unique(y_true)) > 1:
        fpr, tpr, _ = roc_curve(y_true, y_probs)
        auc = roc_auc_score(y_true, y_probs)
        
        plt.figure()
        plt.plot(fpr, tpr, label=f'ROC curve (area = {auc:.2f})')
        plt.plot([0, 1], [0, 1], 'k--')
        plt.xlim([0.0, 1.0])
        plt.ylim([0.0, 1.05])
        plt.xlabel('False Positive Rate')
        plt.ylabel('True Positive Rate')
        plt.title('Receiver Operating Characteristic')
        plt.legend(loc='lower right')
        plt.tight_layout()
        plt.savefig(save_path)
        plt.close()
