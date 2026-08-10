# FastAPI Intro — Course Practice

## About

This is where the actual FastAPI fundamentals got built up before
starting real project work — first on a running `shipment` example that
went through several rounds of refactoring (raw dicts → Pydantic models →
enums → response models), and separately on smaller standalone files for
type hints, path params, and query params.

A second project, [bookshelf-tracker](../bookshelf-tracker), applies these
same concepts to something built from scratch, including a real frontend —
worth checking there for how the patterns hold up outside the course's
own example.

---

## Covered so far

- REST fundamentals + API endpoints
- Path parameters
- Query parameters (including optional params and combining multiple)
- CRUD operations (GET, POST, PUT, PATCH, DELETE)
- `HTTPException` for clean error responses instead of raw 500s
- Pydantic models — `BaseModel`, `Field()` constraints, enums as types
- Splitting a shared `schema.py` from route logic in `main.py`
- Response models (`response_model=`, distinct Create/Update/Read shapes)
- Scalar as an alternative to the default Swagger docs UI

## Structure

```
app/
├── type_hints_refresher.py   # general Python typing practice (prerequisite, not a numbered module)
├── fastapi_intro.py           # first FastAPI app, basic GET route
├── path_parameters.py
├── query_parameter.py
├── simple_database.py         # first pass at an in-memory "database" + basic CRUD
├── http_exception.py          # error handling patterns
├── pydantic.py                # main CRUD app using schema.py's models
└── schema.py                  # Shipment models, enums, Create/Update/Read split
```

## Running

```bash
python3 -m venv venv
source venv/bin/activate
pip install fastapi "fastapi[standard]" scalar_fastapi
fastapi dev app/pydantic.py
```

Docs at `http://127.0.0.1:8000/scalar`

## Key lessons (see `notes.md` for the full list)

- A parameter or variable named the same as an imported module (`status`)
  silently shadows it inside that function — causes `AttributeError`, not
  an obvious import error.
- Primitive types (`str`, `int`, `float`) as bare route parameters default
  to query params, not the request body — need `Body(...)` or a Pydantic
  model to be read from JSON.
- A model reused for PATCH must have every field optional, or the "partial"
  update becomes a disguised full-replace requirement.
- `dict[key]["field"] = value` (dict syntax) and `model.field = value`
  (attribute syntax) are not interchangeable — mixing them on the same
  object is a common source of `TypeError`/`AttributeError` once storage
  switches from raw dicts to actual model instances.
