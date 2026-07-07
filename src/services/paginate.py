
async def paginate(
        smtp,
        parameters: dict,
        cls
):
    size = parameters["size"]
    page = parameters["page"]
    smtp = smtp.offset(page * size - size).limit(size).order_by(cls.id)
    return smtp
