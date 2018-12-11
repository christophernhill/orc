from datetime import datetime
from subprocess import run, PIPE
from os.path import basename, join


def quota():
    """
    This script is called every time nfs-provisioner projects file is changed.

    According to the change in the projects file, adds into /deletes from xfs quota.
    """
    xfs_dir = '/xfs'
    nfs_dir = f'{xfs_dir}/nfs'
    # projects file from xfs-nfs-provisioner
    nfs_projects_path = f'{nfs_dir}/projects'
    print(f'{datetime.utcnow()} [UTC]: {nfs_projects_path} is changed')
    # projects file of quota.py
    projects_path = '/home/iuser/xfs_nfs/projects'

    with open(nfs_projects_path, 'r') as f1, \
         open(projects_path, 'r+') as f2:
        nfs_projects = {l for l in f1.read().splitlines() if l.strip()}
        projects = {l for l in f2.read().splitlines() if l.strip()}

        deleted = projects.difference(nfs_projects)
        for d in deleted:
            print(f'{datetime.utcnow()} [UTC]: deleted project: {d}')
            project_id = d.split(':')[0]
            # remove project from xfs quota by setting hard limit to 0
            cp = run(f"xfs_quota -x -c 'limit -p bhard=0 {project_id}' {xfs_dir}",
                     shell=True, stdout=PIPE, stderr=PIPE)
            print('{} - {} - {} - {}'.format(cp.args, cp.returncode, cp.stdout, cp.stderr))
            projects.remove(d)

        added = nfs_projects.difference(projects)
        for a in added:
            print(f'{datetime.utcnow()} [UTC]: added project: {a}')
            project_id, project_path, hard_limit = a.split(':')
            project_folder = basename(project_path)
            project_path = join(nfs_dir, project_folder)
            # add new project to xfs quota
            cp = run(f"xfs_quota -x -c 'project -s -p {project_path} {project_id}' f'{xfs_dir}",
                     shell=True, stdout=PIPE, stderr=PIPE)
            print('{} - {} - {} - {}'.format(cp.args, cp.returncode, cp.stdout, cp.stderr))
            # set hard limit for this project
            cp = run(f"xfs_quota -x -c 'limit -p bhard={hard_limit} {project_id}' f'{xfs_dir}",
                     shell=True, stdout=PIPE, stderr=PIPE)
            print('{} - {} - {} - {}'.format(cp.args, cp.returncode, cp.stdout, cp.stderr))
            projects.add(a)

        # re-write all projects into projects file of quota.py
        f2.seek(0)
        f2.write('\n'.join(projects) + '\n')
        f2.truncate()


if __name__ == '__main__':
    quota()
