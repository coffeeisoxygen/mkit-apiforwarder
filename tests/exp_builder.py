from urllib.parse import urlencode


def build_query(
    module: dict, product: dict, default_params: dict, action: str, runtime: dict
):
    """
    Build URL & query params dari module + product + default params + runtime.
    """
    dp = default_params[action]

    # copy required params
    params = dp.get("required_params", {}).copy()

    # merge runtime params
    params.update(runtime)

    # override category dari product
    params["category"] = product["product"]

    # pastikan productId tersedia untuk paket action
    if action == "paket" and ("productId" not in params or not params["productId"]):
        raise ValueError("paket action requires runtime 'productId'")

    # join kolom jika ada
    if "kolom" in dp:
        params["kolom"] = ",".join(dp["kolom"])

    # build URL
    url = f"{module['base_url']}{dp['api_path']}?{urlencode(params)}"
    return url, params
