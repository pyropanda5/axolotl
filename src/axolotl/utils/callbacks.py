"""Callbacks for Trainer class"""

import os

from optimum.bettertransformer import BetterTransformer
from transformers import (
    TrainerCallback,
    TrainerControl,
    TrainerState,
    TrainingArguments,
)
from transformers.trainer_utils import PREFIX_CHECKPOINT_DIR


class SavePeftModelCallback(TrainerCallback):  # pylint: disable=too-few-public-methods
    """Callback to save the PEFT adapter"""

    def on_save(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        **kwargs,
    ):
        checkpoint_folder = os.path.join(
            args.output_dir,
            f"{PREFIX_CHECKPOINT_DIR}-{state.global_step}",
        )

        peft_model_path = os.path.join(checkpoint_folder, "adapter_model")
        kwargs["model"].save_pretrained(peft_model_path)

        return control


class SaveBetterTransformerModelCallback(
    TrainerCallback
):  # pylint: disable=too-few-public-methods
    """Callback to save the BatterTransformer wrapped model"""

    def on_save(
        self,
        args: TrainingArguments,
        state: TrainerState,
        control: TrainerControl,
        **kwargs,
    ):
        checkpoint_folder = os.path.join(
            args.output_dir,
            f"{PREFIX_CHECKPOINT_DIR}-{state.global_step}",
        )

        model = BetterTransformer.reverse(kwargs["model"])
        model.save_pretrained(checkpoint_folder)

        return control
