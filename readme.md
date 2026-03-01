## Quick Run

```bash
git clone https://github.com/roumerchi/jfd/
docker compose up
```
Backend API / Swagger Docs: http://localhost:8000/api/docs/
React Frontend: http://localhost:3000

---
## Versions
- Python 3.14
- React 19.2.4
---

## Disclamer
1) The inclusion of jQuery in the task description threw me off—usually, it's used when a project is 
built entirely on pure Django. This led me to think I "should" create separate REST endpoints while
keeping the frontend within Django itself.
2) The Docker build is handled in a single container to make it faster and easier to clean up the "clutter" 
on my local machine afterward.
3) The backend launch is also in "newbie mode." I could use Gunicorn, or even Daphne to slightly
boost RPS, but in that case, FastAPI would be better, since Django—as it turns out—still doesn't fully support true asynchronous mode.