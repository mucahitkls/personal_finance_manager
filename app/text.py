@router.delete("/{user_id}", response_model=user_schema.UserBase)
async def delete_user(user_id: int, current_user: TokenData = Depends(get_current_active_admin)):
    # Your delete logic here
