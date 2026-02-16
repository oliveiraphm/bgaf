from typing import Literal, TypeAlias
from loguru import logger
from dataclasses import dataclass
import tiktoken

SupportedModels: TypeAlias = Literal["gpt-3.5", "gpt-4"]
PriceTable: TypeAlias = dict[SupportedModels, float]
price_table: PriceTable = {"gpt-3.5": 0.0030, "gpt-4": 0.0200}
prices: PriceTable = {"gpt-3.5": 0.0030, "gpt-4": 0.0200}

@dataclass
class Message:
    prompt: str
    response: str | None
    model: SupportedModels

@dataclass
class MessageCostReport:
    req_costs: float
    res_costs: float
    total_costs: float

def count_tokens(text: str | None) -> int:
    if text is None:
        logger.warning("Response is None. Assuming 0 tokens used")
        return 0
    enc = tiktoken.encoding_for_model("gpt-4o")
    return len(enc.encode(text))


#def calculate_usage_costs(
#        prompt: str,
#        response: str | None,
#        model: SupportedModels,
#) -> tuple[float, float, float]:
#    if model not in price_table:
#        raise ValueError(f"Cost calculation is not supported for {model} model.")
#    price = price_table[model]
#    req_costs = price * count_tokens(prompt) / 1000
#    res_costs = price * count_tokens(response) / 1000
#    total_costs = req_costs + res_costs
#    return req_costs, res_costs, total_costs

def calculate_usage_costs(message: Message) -> MessageCostReport:
    if message.model not in prices:
        raise ValueError(
            f"Cost calculation is not supported for {message.model} model."
        )
    price = prices[message.model]
    req_costs = price * count_tokens(message.prompt) / 1000
    res_costs = price * count_tokens(message.response) / 1000
    total_costs = req_costs + res_costs
    return MessageCostReport(
        req_costs=req_costs, res_costs=res_costs, total_costs=total_costs
    )