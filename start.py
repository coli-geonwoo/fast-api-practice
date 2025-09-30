#
# from schemas.todo_schema import
# from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
#
# app = FastAPI(title="Todo API", version="1.0.0")
#
# router = APIRouter(
#     prefix="/todo",
#     tags=["todo"],
#     responses={status.HTTP_404_NOT_FOUND: {"description": "Not found"}}
# )
#
# app.include_router(router)
#
#
# @router.post(
#     "/",  # POST /
#     response_model=Todo,
#     status_code=status.HTTP_201_CREATED,
#     response_model_exclude_none=True,
#     summary="Create a new todo")
# def create_todo(
#         payload: CreateTodoInput,
#         service: TodoService = Depends(get_todo_service)
# ) -> Todo:
#     todo_out = service.create_todo(payload)
#     return todo_out
#
#
# @router.get(
#     "/todos/all",
#     response_model=List[Todo]
# )
# def find_todo(
#         service: TodoService = Depends(get_todo_service)
# ) -> List[Todo]:
#     return service.get_all_todos()
#
#
# @router.get(
#     "/todos/{todo_id}",
#     response_model=Todo
# )
# def find_todo(
#         todo_id: int,
#         service: TodoService = Depends(get_todo_service)
# ) -> Todo:
#     return service.get_todo(todo_id)
#
#
# @router.patch(
#     "/",  # POST /
#     response_model=Todo,
# )
# def update_todo(
#         payload: UpdateTodoInput,
#         service: TodoService = Depends(get_todo_service)
# ) -> Todo:
#     todo_out = service.update_todo(payload)
#     return todo_out
#
#
# @router.delete(
#     "/{todo_id}",  # POST /
#     status_code=status.HTTP_204_NO_CONTENT
# )
# def delete_todo(
#         todo_id: int,
#         service: TodoService = Depends(get_todo_service)
# ):
#     service.delete_todo(todo_id)
#
#
# if __name__ == "__main__":
#     import uvicorn
#
#     uvicorn.run(app, host="0.0.0.0", port=7701)
# # python3 -m uvicorn main:app --host 0.0.0.0 --port 7701 --reload
#
